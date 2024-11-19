import { Weak } from '../../../../helpers'
import { PropsUIPageError } from '../../../../types/pages'
import { ReactFactoryContext } from '../../factory'
import { Page } from './templates/page'
import TextBundle from '../../../../text_bundle'
import { Translator } from '../../../../translator'
import { BodyLarge, Title1 } from '../elements/text'

type Props = Weak<PropsUIPageError> & ReactFactoryContext

export const ErrorPage = (props: Props): JSX.Element => {
  // render to top of the page on reload
  window.scrollTo(0, 0)

  const { stacktrace } = props
  const { title, text } = prepareCopy(props)

  const body: JSX.Element = (
    <>
      <Title1 text={title} />
      <BodyLarge text={text} />
      <BodyLarge text={stacktrace} />
    </>
  )

  return (
    <Page
      body={body}
    />
  )
}

interface Copy {
  title: string
  text: string
}

function prepareCopy ({ locale }: Props): Copy {
  return {
    title: Translator.translate(title, locale),
    text: Translator.translate(text, locale)
  }
}

const title = new TextBundle()
  .add('en', 'Error, not your fault!')
  .add('nl', 'Foutje, niet jouw schuld!')

const text = new TextBundle()
  .add('en', 'Consult the researcher, or close the page')
  .add('nl', 'Raadpleeg de onderzoeker of sluit de pagina')
