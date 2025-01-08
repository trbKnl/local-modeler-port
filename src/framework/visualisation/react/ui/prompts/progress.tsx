import { Weak } from '../../../../helpers'
import { Translator } from '../../../../translator'
import { ReactFactoryContext } from '../../factory'
import { PropsUIPromptProgress } from '../../../../types/prompts'
import { ProgressBar } from '../elements/progress_bar'
import { Spinner } from '../elements/spinner'

type Props = Weak<PropsUIPromptProgress> & ReactFactoryContext

export const Progress = (props: Props): JSX.Element => {
  const { resolve, percentage } = props
  const { description, message } = prepareCopy(props)

  function progressBar (): JSX.Element {
    if (percentage !== undefined) {
      return (
        <>
          <div className='mt-2' />
          <ProgressBar percentage={percentage} />
        </>
      )
    } else {
      return <></>
    }
  }

  function autoResolve(): void {
    resolve?.({ __type__: 'PayloadTrue', value: true })
  }


  // No user action possible, resolve directly to give control back to script
  // set timeout on autoresolve on purpose so screen stays up for at least x ms
  // so user can read the message
  autoResolve()

  return (
    <>
      <div id='select-panel'>
        <div className='text-bodylarge font-body text-grey1 text-left'>
          {description}
        </div>
        <div className='mt-8' />
        <div className='p-6 border-grey4 border-2 rounded flex flex-row gap-4'>
          <Spinner color={'dark'} spinning={true} />
          <div className='text-bodylarge font-body text-grey2 text-left'>
            {message}
          </div>
          {progressBar()}
        </div>
      </div>
    </>
  )
}

interface Copy {
  description: string
  message: string
}

function prepareCopy ({ description, message, locale }: Props): Copy {
  return {
    description: Translator.translate(description, locale),
    message: message
  }
}
