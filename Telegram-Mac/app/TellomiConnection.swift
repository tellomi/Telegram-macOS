import Foundation

enum TellomiConnection {
    static func refuseTelegramDefaults() -> Never {
        let env = ProcessInfo.processInfo.environment
        let dc = env["TELLOMI_DC_CONFIG"] ?? ""
        let key = env["TELLOMI_SERVER_PUBLIC_KEY"] ?? ""
        if dc.isEmpty || key.isEmpty {
            fatalError("Tellomi: MTProto is not implemented. TELLOMI_DC_CONFIG and TELLOMI_SERVER_PUBLIC_KEY are unset, so this process stops before opening a connection and does not use Telegram production datacenters.")
        }
        let dcExists = FileManager.default.fileExists(atPath: dc)
        let keyExists = FileManager.default.fileExists(atPath: key)
        if !dcExists || !keyExists {
            fatalError("Tellomi: MTProto is not implemented. The DC config or server public key path does not exist, so this process stops before opening a connection.")
        }
        fatalError("Tellomi: MTProto wiring is not implemented. The DC config and server public key files exist but are not read into the network stack. This process does not fall back to Telegram production.")
    }
}
