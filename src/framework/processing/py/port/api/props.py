from dataclasses import dataclass
from typing import Optional, TypedDict, Dict, Any

import pandas as pd


class Translations(TypedDict):
    """
    Typed dict containing text that is displayed in a specific language.
    """
    en: str
    nl: str


@dataclass
class Translatable:
    """
    Wrapper class for Translations.
    """
    translations: Translations

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        return self.__dict__.copy()


@dataclass
class PropsUIHeader:
    """
    Page header.
    """
    title: Translatable

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIHeader"
        dict["title"] = self.title.toDict()
        return dict


@dataclass
class PropsUIFooter:
    """
    Page footer.
    """
    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIFooter"
        return dict


@dataclass
class PropsUIPromptConfirm:
    """
    Retry submitting a file page.

    Prompt the user if they want to submit a new file.
    This can be used in case a file could not be processed.

    Attributes:
        text (Translatable): Message to display.
        ok (Translatable): Message to display if the user wants to try again.
        cancel (Translatable): Message to display if the user wants to continue regardless.
    """
    text: Translatable
    ok: Translatable
    cancel: Translatable

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPromptConfirm"
        dict["text"] = self.text.toDict()
        dict["ok"] = self.ok.toDict()
        dict["cancel"] = self.cancel.toDict()
        return dict


@dataclass
class PropsUIPromptConsentFormTable:
    """
    Table to be shown to the participant prior to donation.

    Attributes:
        id (str): A unique string to identify the table after donation.
        title (Translatable): Title of the table.
        data_frame (pd.DataFrame | Dict[str, Dict[str, Any]]): Table to be shown can be a pandas DataFrame or a dictionary.
        description (Optional[Translatable]): Optional description of the table.
        visualizations (Optional[list]): Optional visualizations to be shown.
        folded (Optional[bool]): Whether the table should be initially folded.
        delete_option (Optional[bool]): Whether to show a delete option for the table.

    Examples::

        data_frame_df = pd.DataFrame([
            {"column1": 1, "column2": 4},
            {"column1": 2, "column2": 5},
            {"column1": 3, "column2": 6},
        ])
        
        example1 = PropsUIPromptConsentFormTable(
            id="example1",
            title=Translatable("Table as DataFrame"),
            data_frame=data_frame_df,
        )

        data_frame_dict = {
            "column1": {"0": 1, "1": 4},
            "column2": {"0": 2, "1": 5},
            "column3": {"0": 3, "1": 6},
        }
        
        example2 = PropsUIPromptConsentFormTable(
            id="example2",
            title=Translatable("Table as Dictionary"),
            data_frame=data_frame_dict,
        )
    """
    id: str
    title: Translatable
    data_frame: pd.DataFrame | Dict[str, Dict[str, Any]]
    description: Optional[Translatable] = None
    visualizations: Optional[list] = None
    folded: Optional[bool] = False
    delete_option: Optional[bool] = True

    def translate_data_frame(self):
        if isinstance(self.data_frame, pd.DataFrame):
            return self.data_frame.to_json()
        else:
            return self.data_frame

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPromptConsentFormTable"
        dict["id"] = self.id
        dict["title"] = self.title.toDict()
        dict["data_frame"] = self.translate_data_frame()
        dict["description"] = self.description.toDict() if self.description else None
        dict["visualizations"] = self.visualizations if self.visualizations else None
        dict["folded"] = self.folded
        dict["delete_option"] = self.delete_option
        return dict


@dataclass
class PropsUIPromptConsentForm:
    """
    Tables to be shown to the participant prior to donation.

    Attributes:
        id (str): will be used as part of the filename when the data is stored
        tables (list[PropsUIPromptConsentFormTable]): A list of tables.
        meta_tables (list[PropsUIPromptConsentFormTable]): A list of optional tables, for example for logging data.
        description (Optional[Translatable]): Optional description of the consent form.
        donate_question (Optional[Translatable]): Optional donation question.
        donate_button (Optional[Translatable]): Optional text for the donate button.
    """
    id: str
    tables: list[PropsUIPromptConsentFormTable]
    meta_tables: list[PropsUIPromptConsentFormTable]
    description: Optional[Translatable] = None
    donate_question: Optional[Translatable] = None
    donate_button: Optional[Translatable] = None

    def translate_tables(self):
        """
        Translate the tables to a list of dictionaries.

        Returns:
            list: A list of dictionaries representing the tables.
        """
        output = []
        for table in self.tables:
            output.append(table.toDict())
        return output

    def translate_meta_tables(self):
        """
        Translate the meta tables to a list of dictionaries.

        Returns:
            list: A list of dictionaries representing the meta tables.
        """
        output = []
        for table in self.meta_tables:
            output.append(table.toDict())
        return output

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPromptConsentForm"
        dict["id"] = self.id
        dict["tables"] = self.translate_tables()
        dict["metaTables"] = self.translate_meta_tables()
        dict["description"] = self.description and self.description.toDict()
        dict["donateQuestion"] = self.donate_question and self.donate_question.toDict()
        dict["donateButton"] = self.donate_button and self.donate_button.toDict()
        return dict


@dataclass
class PropsUIPromptFileInput:
    """
    Prompt the user to submit a file.

    Attributes:
        description (Translatable): Text with an explanation.
        extensions (str): Accepted mime types, example: "application/zip, text/plain".
    """
    description: Translatable
    extensions: str

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPromptFileInput"
        dict["description"] = self.description.toDict()
        dict["extensions"] = self.extensions
        return dict


@dataclass
class PropsUIPromptFileInputMultiple:
    """
    Prompt the user to submit multiple files.

    Attributes:
        description (Translatable): Text with an explanation.
        extensions (str): Accepted mime types, example: "application/zip, text/plain".
    """
    description: Translatable
    extensions: str

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPromptFileInputMultiple"
        dict["description"] = self.description.toDict()
        dict["extensions"] = self.extensions
        return dict


@dataclass
class PropsUIPromptProgress:
    """
    Prompt the user information during the extraction.

    Attributes:
        description (Translatable): Text with an explanation.
        message (str): Can be used to show extraction progress.
        percentage (Optional[int]): Optional percentage of progress.
    """
    description: Translatable
    message: str
    percentage: Optional[int] = None

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPromptProgress"
        dict["description"] = self.description.toDict()
        dict["message"] = self.message
        dict["percentage"] = self.percentage
        return dict


class RadioItem(TypedDict):
    """
    Radio button.

    Attributes:
        id (int): ID of radio button.
        value (str): Text to be displayed.
    """
    id: int
    value: str


@dataclass
class PropsUIPromptRadioInput:
    """
    Radio group.

    This radio group can be used to get a multiple choice answer from a user.

    Attributes:
        title (Translatable): Title of the radio group.
        description (Translatable): Short description of the radio group.
        items (list[RadioItem]): A list of radio buttons.
    """
    title: Translatable
    description: Translatable
    items: list[RadioItem]

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPromptRadioInput"
        dict["title"] = self.title.toDict()
        dict["description"] = self.description.toDict()
        dict["items"] = self.items
        return dict


@dataclass
class PropsUIQuestionOpen:
    """
    Open-ended question.

    Attributes:
        id (int): Question ID.
        question (Translatable): The question text.
    """
    id: int
    question: Translatable

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIQuestionOpen"
        dict["id"] = self.id
        dict["question"] = self.question.toDict()
        return dict


@dataclass
class PropsUIQuestionMultipleChoiceCheckbox:
    """
    Multiple choice question with checkboxes.

    Attributes:
        id (int): Question ID.
        question (Translatable): The question text.
        choices (list[Translatable]): List of choices.
    """
    id: int
    question: Translatable
    choices: list[Translatable]

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIQuestionMultipleChoiceCheckbox"
        dict["id"] = self.id
        dict["question"] = self.question.toDict()
        dict["choices"] = [c.toDict() for c in self.choices]
        return dict


@dataclass
class PropsUIQuestionMultipleChoice:
    """
    Multiple choice question with radio buttons.

    Attributes:
        id (int): Question ID.
        question (Translatable): The question text.
        choices (list[Translatable]): List of choices.
    """
    id: int
    question: Translatable
    choices: list[Translatable]

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIQuestionMultipleChoice"
        dict["id"] = self.id
        dict["question"] = self.question.toDict()
        dict["choices"] = [c.toDict() for c in self.choices]
        return dict


@dataclass
class PropsUIPromptQuestionnaire:
    """
    Questionnaire containing multiple questions.

    Attributes:
        description (Translatable): Description of the questionnaire.
        questions (list[PropsUIQuestionMultipleChoice | PropsUIQuestionMultipleChoiceCheckbox | PropsUIQuestionOpen]):
            List of questions in the questionnaire.
    """
    description: Translatable
    questions: list[PropsUIQuestionMultipleChoice | PropsUIQuestionMultipleChoiceCheckbox | PropsUIQuestionOpen]

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPromptQuestionnaire"
        dict["description"] = self.description.toDict()
        dict["questions"] = [q.toDict() for q in self.questions]
        return dict


@dataclass
class PropsUIPageDonation:
    """
    A multi-purpose page that gets shown to the user.

    Attributes:
        platform (str): 
            The platform name the user is currently in the process of donating data from.
        header (PropsUIHeader): Page header.
        body (PropsUIPromptRadioInput | PropsUIPromptConsentForm |
            PropsUIPromptFileInput | PropsUIPromptFileInputMultiple | 
            PropsUIPromptConfirm | PropsUIPromptQuestionnaire):
            Main body of the page.
        footer (Optional[PropsUIFooter]): Optional page footer.
    """
    platform: str
    header: PropsUIHeader
    body: (
        PropsUIPromptRadioInput
        | PropsUIPromptConsentForm
        | PropsUIPromptFileInput
        | PropsUIPromptFileInputMultiple
        | PropsUIPromptConfirm
        | PropsUIPromptQuestionnaire
    )
    footer: Optional[PropsUIFooter] = None

    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPageDonation"
        dict["platform"] = self.platform
        dict["header"] = self.header.toDict()
        dict["body"] = self.body.toDict()
        dict["footer"] = self.footer.toDict() if self.footer else None
        return dict


class PropsUIPageEnd:
    """
    An ending page to show the user they are done.
    """
    def toDict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        dict = {}
        dict["__type__"] = "PropsUIPageEnd"
        return dict
