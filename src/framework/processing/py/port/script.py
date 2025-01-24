import logging
import json
import io
from typing import Tuple
import time

import pandas as pd

from port.api.commands import (CommandSystemDonate, CommandSystemExit, CommandUIRender)
import port.api.props as props
import port.instagram as instagram
import port.helpers.validate as validate
import port.lda as lda
import port.average as average
#import port.ols as ols


LOG_STREAM = io.StringIO()

logging.basicConfig(
    stream=LOG_STREAM,
    level=logging.INFO,
    format="%(asctime)s --- %(name)s --- %(levelname)s --- %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)

LOGGER = logging.getLogger("script")

# Headers
SUBMIT_FILE_HEADER = props.Translatable({
    "en": "Select your Instagram file", 
    "nl": "Selecteer uw Instagram bestand"
})

REVIEW_DATA_HEADER = props.Translatable({
    "en": "Your Instagram data", 
    "nl": "Uw Instagram gegevens"
})

RETRY_HEADER = props.Translatable({
    "en": "Try again", 
    "nl": "Probeer opnieuw"
})

PLEASE_WAIT_HEADER = props.Translatable({
    "en": "We are learning from your data", 
    "nl": "We zijn aan het leren van uw data"
})


def process(session_id):
    LOGGER.info("Starting the donation flow")
    yield donate_logs(f"{session_id}-tracking")


    platform_name = "Instagram"
    table_list = None
    document = None
    following_followers_tuple = None

    while True:
        LOGGER.info("Prompt for file for %s", platform_name)
        yield donate_logs(f"{session_id}-tracking")

        file_prompt = generate_file_prompt("application/zip")
        file_result = yield render_page(SUBMIT_FILE_HEADER, file_prompt)

        if file_result.__type__ == "PayloadString":
            validation = validate.validate_zip(instagram.DDP_CATEGORIES, file_result.value)

            # Flow logic
            # Happy flow: Valid DDP
            if validation.get_status_code_id() == 0:
                LOGGER.info("Payload for %s", platform_name)
                yield donate_logs(f"{session_id}-tracking")

                extraction_result, document, following_followers_tuple = extract_instagram(file_result.value)
                table_list = extraction_result
                break

            # Enter retry flow, reason: if DDP was not a Instagram DDP
            if validation.get_status_code_id != 0:
                LOGGER.info("Not a valid %s zip; No payload; prompt retry_confirmation", platform_name)
                yield donate_logs(f"{session_id}-tracking")
                retry_result = yield render_page(RETRY_HEADER, retry_confirmation(platform_name))

                if retry_result.__type__ == "PayloadTrue":
                    continue
                else:
                    LOGGER.info("Skipped during retry flow")
                    yield donate_logs(f"{session_id}-tracking")
                    yield donate_status(f"{session_id}-SKIP-RETRY-FLOW", "SKIP_RETRY_FLOW")
                    break

        else:
            LOGGER.info("Skipped at file selection ending flow")
            yield donate_logs(f"{session_id}-tracking")
            yield donate_status(f"{session_id}-SKIP-FILE-SELECTION", "SKIP_FILE_SELECTION")
            break


    if table_list is not None:
        LOGGER.info("Prompt consent; %s", platform_name)
        yield donate_logs(f"{session_id}-tracking")
        prompt = create_consent_form(table_list)
        consent_result = yield render_page(REVIEW_DATA_HEADER, prompt)

        # Data was donated
        if consent_result.__type__ == "PayloadJSON":
            LOGGER.info("Data donated; %s", platform_name)
            yield donate(f"{session_id}-{platform_name}", consent_result.value)
            yield donate_logs(f"{session_id}-tracking")
            yield donate_status(f"{session_id}-DONATED", "DONATED")

    start_time = time.time()
    if document is not None:
        message = prompt_extraction_message("Please wait")
        yield render_page(PLEASE_WAIT_HEADER, message)
        
        # Run lda
        study_id = "ldafive"
        run = yield lda.getParameters(study_id)
        while run.__type__ != "PayloadError": 
            yield lda.putParameters(run.value, 5, [document], study_id)
            run = yield lda.getParameters(study_id)
        
        study_id = "ldaten"
        run = yield lda.getParameters(study_id)
        while run.__type__ != "PayloadError": 
            yield lda.putParameters(run.value, 10, [document], study_id)
            run = yield lda.getParameters(study_id)

        study_id = "ldatwentyfive"
        run = yield lda.getParameters(study_id)
        while run.__type__ != "PayloadError": 
            yield lda.putParameters(run.value, 25, [document], study_id)
            run = yield lda.getParameters(study_id)

    # Run Average
    study_id = "averagefollowing"
    if following_followers_tuple is not None:
        following_count, _ = following_followers_tuple
        if following_count != "Unkowwn":
            run = yield average.getParameters(study_id)
            while run.__type__ != "PayloadError": 
                yield average.putParameters(run.value, following_count, study_id)
                run = yield average.getParameters(study_id)

    study_id = "averagefollowers"
    if following_followers_tuple is not None:
        _, followers_count = following_followers_tuple
        if followers_count != "Unkowwn":
            run = yield average.getParameters(study_id)
            while run.__type__ != "PayloadError": 
                yield average.putParameters(run.value, followers_count, study_id)
                run = yield average.getParameters(study_id)

    # Run OLS
    # study is called "regression"
    #run = yield ols.getParameters()
    #while run.__type__ != "PayloadError": 
    #    yield ols.putParameters(run.value)
    #    run = yield ols.getParameters()
    while time.time() - start_time < 8:
        time.sleep(0.1) 

    yield exit(0, "Success")
    yield render_end_page()


##################################################################

def create_consent_form(table_list: list[props.PropsUIPromptConsentFormTable]) -> props.PropsUIPromptConsentForm:
    """
    Assembles all donated data in consent form to be displayed
    """
    return props.PropsUIPromptConsentForm("instagram", tables=table_list, meta_tables=[])


def donate_logs(key):
    log_string = LOG_STREAM.getvalue()  # read the log stream
    if log_string:
        log_data = log_string.split("\n")
    else:
        log_data = ["no logs"]

    return donate(key, json.dumps(log_data))


def donate_status(filename: str, message: str):
    return donate(filename, json.dumps({"status": message}))


def render_end_page():
    page = props.PropsUIPageEnd()
    return CommandUIRender(page)


def render_page(header_text, body):
    header = props.PropsUIHeader(header_text)

    footer = props.PropsUIFooter()
    platform = "Instagram"
    page = props.PropsUIPageDonation(platform, header, body, footer)
    return CommandUIRender(page)


def retry_confirmation(platform):
    text = props.Translatable(
        {
            "en": f"Unfortunately, we could not process your {platform} file. If you are sure that you selected the correct file, press Continue. To select a different file, press Try again.",
            "nl": f"Helaas, kunnen we uw {platform} bestand niet verwerken. Weet u zeker dat u het juiste bestand heeft gekozen? Ga dan verder. Probeer opnieuw als u een ander bestand wilt kiezen."
        }
    )
    ok = props.Translatable({"en": "Try again", "nl": "Probeer opnieuw"})
    cancel = props.Translatable({"en": "Continue", "nl": "Verder"})
    return props.PropsUIPromptConfirm(text, ok, cancel)



##################################################################
# Extraction function


def extract_instagram(instagram_zip: str):
    tables_to_render = []
    lda_dfs = []

    df = instagram.posts_viewed_to_df(instagram_zip)
    if not df.empty:
        table_title = props.Translatable({
            "en": "Posts viewed on Instagram",
            "nl": "Posts viewed on Instagram"
        })
        table_description = props.Translatable({
            "en": "In this table you find the accounts of posts you viewed on Instagram sorted over time. Below, you find visualizations of different parts of this table. First, you find a timeline showing you the number of posts you viewed over time. Next, you find a histogram indicating how many posts you have viewed per hour of the day.", 
            "nl": "In this table you find the accounts of posts you viewed on Instagram sorted over time. Below, you find visualizations of different parts of this table. First, you find a timeline showing you the number of posts you viewed over time. Next, you find a histogram indicating how many posts you have viewed per hour of the day.", 
        })
        table =  props.PropsUIPromptConsentFormTable("instagram_posts_viewed", table_title, df, table_description, []) 
        tables_to_render.append(table)
        lda_dfs.append(df)

    df = instagram.videos_watched_to_df(instagram_zip)
    if not df.empty:
        table_title = props.Translatable({
            "en": "Videos watched on Instagram",
            "nl": "Videos watched on Instagram"
        })
        table_description = props.Translatable({
            "en": "In this table you find the accounts of videos you watched on Instagram sorted over time. Below, you find a timeline showing you the number of videos you watched over time.", 
            "nl": "In this table you find the accounts of videos you watched on Instagram sorted over time. Below, you find a timeline showing you the number of videos you watched over time. ", 
        })

        table =  props.PropsUIPromptConsentFormTable("instagram_videos_watched", table_title, df, table_description, []) 
        tables_to_render.append(table)
        lda_dfs.append(df)


    df = instagram.post_comments_to_df(instagram_zip)
    if not df.empty:
        table_title = props.Translatable({
            "en": "Comments on Instagram posts",
            "nl": "Comments on Instagram posts",
        })
        table_description = props.Translatable({
            "en": "In this table, you find the comments that you left behind on Instagram posts sorted over time. Below, you find a wordcloud, where the size of the word indicates how frequently that word has been used in these comments.", 
            "nl": "In this table, you find the comments that you left behind on Instagram posts sorted over time. Below, you find a wordcloud, where the size of the word indicates how frequently that word has been used in these comments.", 
        })
        table =  props.PropsUIPromptConsentFormTable("instagram_post_comments", table_title, df, table_description, []) 
        tables_to_render.append(table)
        lda_dfs.append(df)

    df = instagram.accounts_not_interested_in_to_df(instagram_zip)
    if not df.empty:
        table_title = props.Translatable({
            "en": "Instagram accounts not interested in",
            "nl": "Instagram accounts not interested in"
        })
        table_description = props.Translatable({
            "en": "", 
            "nl": "", 
        })
        table =  props.PropsUIPromptConsentFormTable("instagram_accounts_not_interested_in", table_title, df, table_description) 
        tables_to_render.append(table)

    df = instagram.posts_not_interested_in_to_df(instagram_zip)
    if not df.empty:
        table_title = props.Translatable({
            "en": "Instagram posts not interested in",
            "nl": "Instagram posts not interested in"
        })
        table_description = props.Translatable({
            "en": "", 
            "nl": "", 
        })
        table =  props.PropsUIPromptConsentFormTable("instagram_posts_not_interested_in", table_title, df, table_description) 
        tables_to_render.append(table)


    df = instagram.following_to_df(instagram_zip)
    if not df.empty:
        table_title = props.Translatable({
            "en": "Accounts that you follow on Instagram",
            "nl": "Accounts that you follow on Instagram"
        })
        table_description = props.Translatable({
            "en": "In this table, you find the accounts that you follow on Instagram.", 
            "nl": "In this table, you find the accounts that you follow on Instagram.", 
        })
        table =  props.PropsUIPromptConsentFormTable("instagram_following", table_title, df, table_description) 
        tables_to_render.append(table)
        df['count'] = 1
        lda_dfs.append(df)

    df = instagram.liked_comments_to_df(instagram_zip)
    if not df.empty:
        table_title = props.Translatable({
            "en": "Instagram liked comments",
            "nl": "Instagram liked comments",
        })
        table_description = props.Translatable({
            "en": "", 
            "nl": "", 
        })
        table =  props.PropsUIPromptConsentFormTable("instagram_liked_comments", table_title, df, table_description, []) 
        tables_to_render.append(table)


    df, following_followers_tuple = instagram.n_following_followers_to_df(instagram_zip)
    if not df.empty:
        table_title = props.Translatable({
            "en": "Number of following and followers",
            "nl": "Number of following and followers",
        })
        table_description = props.Translatable({
            "en": "", 
            "nl": "", 
        })
        table =  props.PropsUIPromptConsentFormTable("instagram_n_following_followers", table_title, df, table_description, []) 
        tables_to_render.append(table)

    df = instagram.liked_posts_to_df(instagram_zip)
    if not df.empty:
        table_description = props.Translatable({
            "en": "", 
            "nl": "", 
        })
        table_title = props.Translatable({
            "en": "Instagram liked posts",
            "nl": "Instagram liked posts",
        })
        table_description = props.Translatable({
            "en": "", 
            "nl": "", 
        })
        table =  props.PropsUIPromptConsentFormTable("instagram_liked_posts", table_title, df, table_description, []) 
        tables_to_render.append(table)
        df = df.drop("Value", axis=1)
        lda_dfs.append(df)


    document = ""

    try:
        dfs = [
            df.rename(columns={col: f"col_{i+1}" for i, col in enumerate(df.columns)})
            for df in lda_dfs
        ]

        df = pd.concat(dfs, ignore_index=True)
        word_counts = [tuple(row) for row in df.values]
        document = " ".join([word for word, count in word_counts for _ in range(count)])

    except Exception as e:
        LOGGER.info("Could not create document: %s", e)

    return (tables_to_render, document, following_followers_tuple)



##################################################################

def generate_file_prompt(extensions):
    description = props.Translatable(
        {
            "en": f"Please follow the download instructions and choose the file that you stored on your device.",
            "nl": f"Volg de download instructies en kies het bestand dat u opgeslagen heeft op uw apparaat."
        }
    )
    return props.PropsUIPromptFileInput(description, extensions)


def donate(key, json_string):
    return CommandSystemDonate(key, json_string)

def exit(code, info):
    return CommandSystemExit(code, info)


def prompt_extraction_message(message):
    description = props.Translatable({
        "en": "We are learning from your data. Please wait, this can take up to 5 minutes.",
        "nl": "We zijn aan het leren van uw data, nog even wachten alstublieft, dit duurt maximaal 5 minuten."
    })

    return props.PropsUIPromptProgress(description, message)


