#import <Foundation/Foundation.h>

/// Tellomi MTProto settings compiled from tellomi/server/tellomi-server.json.
/// That JSON file is the only place the seed addresses, port and RSA public keys are set.
/// tellomi/apply_mtproto.py copies these sources into the telegram-ios checkout before a build.
NS_ASSUME_NONNULL_BEGIN

/// Datacenter id -> IP literals. `testingEnvironment` selects the JSON's testing or production list.
NSDictionary<NSNumber *, NSArray<NSString *> *> *TellomiSeedAddresses(bool testingEnvironment);

/// TCP port for every seed address.
uint16_t TellomiSeedPort(void);

/// Datacenter id recorded in the JSON. Release builds still open DC 2 first; both DCs use the same seed.
NSInteger TellomiDefaultDatacenterId(void);

/// When true, the client does not resolve Telegram's backup addresses.
bool TellomiDisablesTelegramBackupDiscovery(void);

/// PKCS#1 PEM public keys for the production or the testing environment. Newest first.
NSArray<NSString *> *TellomiServerPublicKeys(bool isProduction);

NS_ASSUME_NONNULL_END
