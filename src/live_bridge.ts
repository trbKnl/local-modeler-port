import { 
  CommandSystem, 
  isCommandSystemGetParameters,
  isCommandSystemPutParameters,
} from './framework/types/commands'
import { Bridge } from './framework/types/modules'

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

  async send (command: CommandSystem): Promise<any> {
    if (isCommandSystemGetParameters(command)) {
      return await this.fetchData(command)
    } else if (isCommandSystemPutParameters(command)) {
      return await this.fetchData(command)
    } else {
      this.log('info', 'send', command)
      this.port.postMessage(command)
    }
  }

  private log (level: 'info' | 'error', ...message: any[]): void {
    const logger = level === 'info' ? console.log : console.error
    logger('[LiveBridge]', ...message)
  }

  async fetchData(command: CommandSystem, timeOut: number = 5000): Promise<any> {
   /**
   * Waits for a specific message on the MessagePort matching the given command.
   *
   * @param command - The command to send and match against the received message.
   * @param timeOut - Timeout in ms
   * @returns A promise that resolves with the data from the matching message.
   */
    return new Promise((resolve) => {
      const action = command.__type__

      const timeoutId = setTimeout(() => {
        window.removeEventListener('message', messageHandler)
        console.log("[LiveBridge] Server timeout: could not resolve action")
        resolve({"__type__": "PayloadError", "value": "Server timeout"})
      }, timeOut)

      const messageHandler = (event: MessageEvent) => {
        if (event.data.action == action) {
          clearTimeout(timeoutId)
          window.removeEventListener('message', messageHandler)
          console.log(`[LiveBridge] action: ${action} resolved`)
          resolve(event.data.data) 
        }
      }

      window.addEventListener('message', messageHandler)
      this.port.postMessage(command)

    })
  }
}

