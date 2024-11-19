import React from 'react';
import { ReactFactoryContext } from '../../factory'
import { Weak } from '../../../../helpers'
import TextBundle from '../../../../text_bundle'
import { PrimaryButton } from '../elements/button'
import { PropsUIPromptQuestionnaire } from '../../../../types/prompts'
import { Translator } from '../../../../translator'
import { isPropsUIQuestionMultipleChoice } from '../../../../types/elements'
import { isPropsUIQuestionMultipleChoiceCheckbox } from '../../../../types/elements'
import { isPropsUIQuestionOpen } from '../../../../types/elements'
import { MultipleChoiceQuestion } from '../../ui/elements/question_multiple_choice'
import { MultipleChoiceQuestionCheckbox } from '../../ui/elements/question_multiple_choice_checkbox'
import { OpenQuestion } from '../../ui/elements/question_open'

type Props = Weak<PropsUIPromptQuestionnaire> & ReactFactoryContext

export const Questionnaire = (props: Props): JSX.Element => {
  const { questions, description, resolve, locale } = props
  const [answers, setAnswers] = React.useState<{}>({});
  const copy = prepareCopy(locale)

    
  React.useEffect(() => {
    // check if running in an iframe
    if (window.frameElement) {
      window.parent.scrollTo(0,0)
    } else {
      window.scrollTo(0,0)
    }
  }, [])

  function handleDonate (): void {
    const value = JSON.stringify(answers)
    resolve?.({ __type__: 'PayloadJSON', value })
  }

  function handleCancel (): void {
    resolve?.({ __type__: 'PayloadFalse', value: false })
  }

  const renderQuestion = (item: any) => {
    if (isPropsUIQuestionMultipleChoice(item)) {
      return (
        <div key={item.id}>
          <MultipleChoiceQuestion {...item} locale={locale} parentSetter={setAnswers} />
        </div>
      )
    }
    if (isPropsUIQuestionMultipleChoiceCheckbox(item)) {
      return (
        <div key={item.id}>
          <MultipleChoiceQuestionCheckbox {...item} locale={locale} parentSetter={setAnswers} />
        </div>
      )
    }
    if (isPropsUIQuestionOpen(item)) {
      return (
        <div key={item.id}>
          <OpenQuestion {...item} locale={locale} parentSetter={setAnswers} />
        </div>
      )
    }
  }

  const renderQuestions = () => {
   return questions.map((item) => renderQuestion(item))
  }

  return (
    <div>
      <div className='flex-wrap text-bodylarge font-body text-grey1 text-left'>
        {copy.description}
      </div>
      <div>
        {renderQuestions()}
      </div>
      <div className='flex flex-row gap-4 mt-4 mb-4'>
        <PrimaryButton label={copy.continueLabel} onClick={handleDonate} color='bg-success text-white' />
      </div>
    </div>
  );

        
  function prepareCopy (locale: string): Copy {
    return {
      description: Translator.translate(description, locale),
      continueLabel: Translator.translate(continueLabel, locale)
    }
  }
};


interface Copy {
  description: string
  continueLabel: string
}


const continueLabel = new TextBundle()
  .add('en', 'Continue')
  .add('nl', 'Verder')
