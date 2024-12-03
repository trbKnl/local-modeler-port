import { Payload, CommandSystem, CommandSystemDonate, CommandSystemExit, isCommandSystemDonate, isCommandSystemExit } from './framework/types/commands'

export default class FakeBridge {
  send (command: CommandSystem): Promise<Payload> {
    if (isCommandSystemDonate(command)) {
      this.handleDonation(command)
    } else if (isCommandSystemExit(command)) {
      this.handleExit(command)
    } else {
      console.log('[FakeBridge] received unknown command: ' + JSON.stringify(command))
    }
    return Promise.resolve({"__type__": "PayloadVoid", "value": undefined});
  }

  handleDonation (command: CommandSystemDonate): void {
    console.log(`[FakeBridge] received donation: ${command.key}=${command.json_string}`)
  }

  handleExit (command: CommandSystemExit): void {
    console.log(`[FakeBridge] received exit: ${command.code}=${command.info}`)
  }
}
