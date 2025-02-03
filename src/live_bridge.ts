import { 
  CommandSystem, 
  isCommandSystemGetParameters,
  isCommandSystemPutParameters,
  Payload,
} from './framework/types/commands'
import { Bridge } from "./framework/types/modules"

export default class LiveBridge implements Bridge {
  port: MessagePort

  constructor (port: MessagePort) {
    this.port = port
  }

  static create (window: Window, callback: (bridge: Bridge, locale: string) => void): void {
    window.addEventListener('message', (event) => {

      if (event.data.action === 'live-init') {
        const bridge = new LiveBridge(event.ports[0])
        const locale = event.data.locale
        console.log('LOCALE', locale)
        callback(bridge, locale)
      }
    })
  }

  async send(command: CommandSystem): Promise<Payload> {
    if (isCommandSystemGetParameters(command) || isCommandSystemPutParameters(command)) {
      return this.fetchData(command)
    } else {
      this.log('info', 'send', command);
      this.port.postMessage(command)
      return { "__type__": "PayloadVoid", value: undefined }
    }
  }

  private log (level: 'info' | 'error', ...message: any[]): void {
    const logger = level === 'info' ? console.log : console.error
    logger('[LiveBridge]', ...message)
  }

  // abuse of any, but the typesystem is really working against me atm
  async fetchData(command: CommandSystem | any, timeOut: number = 10000): Promise<Payload> {
   /**
   * Waits for a specific message on the MessagePort matching the given command.
   *
   * @param command - The command to send and match against the received message.
   * @param timeOut - Timeout in ms
   * @returns A promise that resolves with the data from the matching message.
   */
    return new Promise((resolve) => {
      const action = command.__type__
      const action_id = crypto.randomUUID();
      command["action_id"] = action_id

      const timeoutId = setTimeout(() => {
        window.removeEventListener('message', messageHandler)
        console.log("[LiveBridge] Server timeout: could not resolve action")

        resolve({"__type__": "PayloadError", "value": "Server timeout"})
      }, timeOut)

      const messageHandler = (event: MessageEvent) => {
        if (event.data.action == action && event.data.action_id == action_id) {
          clearTimeout(timeoutId)
          window.removeEventListener('message', messageHandler)
          console.log(`[LiveBridge] action: ${action} resolved`)

          // could add checking "isPayload",
          // however, the type system is annoying it needs to be changed to something like zod
          resolve(event.data.data) 
        } else {
          console.log(`[LiveBridge] action: ${action} with ${action_id} was rejected!`)
        }
      }

      window.addEventListener('message', messageHandler)
      this.port.postMessage(command)

    })
  }
}

