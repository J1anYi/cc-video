// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "CCVideoSDK",
    platforms: [.iOS(.v14), .macOS(.v11)],
    products: [
        .library(name: "CCVideoSDK", targets: ["CCVideoSDK"]),
    ],
    dependencies: [
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0"),
    ],
    targets: [
        .target(
            name: "CCVideoSDK",
            dependencies: ["Alamofire"],
            path: "Sources"
        ),
        .testTarget(name: "CCVideoSDKTests", dependencies: ["CCVideoSDK"]),
    ]
)
