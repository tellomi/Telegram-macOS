import Foundation

enum TellomiConnection {
    static func refuseTelegramDefaults() -> Never {
        let env = ProcessInfo.processInfo.environment
        let dc = env["TELLOMI_DC_CONFIG"] ?? ""
        let key = env["TELLOMI_SERVER_PUBLIC_KEY"] ?? ""
        if dc.isEmpty || key.isEmpty {
            fatalError("Tellomi: set TELLOMI_DC_CONFIG and TELLOMI_SERVER_PUBLIC_KEY to existing files. This build does not use Telegram production datacenters or keys.")
        }
        let dcExists = FileManager.default.fileExists(atPath: dc)
        let keyExists = FileManager.default.fileExists(atPath: key)
        if !dcExists || !keyExists {
            fatalError("Tellomi: DC config or server public key file is missing. Refusing Telegram production defaults.")
        }
        fatalError("Tellomi: connection files are present, but this build does not apply them to MTProto yet and will not fall back to Telegram production.")
    }
}
