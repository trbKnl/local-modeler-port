import { isInstanceOf } from '../helpers'
import { 
    PropsUIHeader,
    PropsUIFooter
} from './elements'
import { 
    PropsUIPromptFileInput, 
    PropsUIPromptFileInputMultiple, 
    PropsUIPromptConfirm,
    PropsUIPromptConsentForm,
    PropsUIPromptRadioInput,
    PropsUIPromptQuestionnaire,
    PropsUIPromptProgress
} from './prompts'

export type PropsUIPage =
  PropsUIPageSplashScreen |
  PropsUIPageDonation |
  PropsUIPageEnd |
  PropsUIPageError

export function isPropsUIPage (arg: any): arg is PropsUIPage {
  return (
    isPropsUIPageDonation(arg) ||
    isPropsUIPageEnd(arg) ||
    isPropsUIPageError(arg)
  )
}

export interface PropsUIPageSplashScreen {
  __type__: 'PropsUIPageSplashScreen'
}

export interface PropsUIPageDonation {
  __type__: 'PropsUIPageDonation'
  platform: string
  header: PropsUIHeader
  body: PropsUIPromptFileInput | PropsUIPromptConfirm | PropsUIPromptProgress | PropsUIPromptConsentForm | PropsUIPromptRadioInput | PropsUIPromptQuestionnaire | PropsUIPromptFileInputMultiple
  footer: PropsUIFooter
}
export function isPropsUIPageDonation (arg: any): arg is PropsUIPageDonation {
  return isInstanceOf<PropsUIPageDonation>(arg, 'PropsUIPageDonation', ['platform', 'header', 'body'])
}

export interface PropsUIPageEnd {
  __type__: 'PropsUIPageEnd'
}
export function isPropsUIPageEnd (arg: any): arg is PropsUIPageEnd {
  return isInstanceOf<PropsUIPageEnd>(arg, 'PropsUIPageEnd', [])
}

export interface PropsUIPageError {
  __type__: 'PropsUIPageError'
  stacktrace: string
}
export function isPropsUIPageError (arg: any): arg is PropsUIPageError {
  return isInstanceOf<PropsUIPageError>(arg, 'PropsUIPageError', ['stacktrace'])
}
