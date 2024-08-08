---
layout: default
title: Snapp Mobile iOS Newsletter 2
issue: 2
date: 2024-08-09
---
## Swift

### [Using @DebugDescription in Xcode 16](https://digitalbunker.dev/debug-description-macro-xcode-16/)

Debugging can be tricky, especially with custom types. Clear and informative debug output is essential for understanding the behavior of your code. That's where the `CustomDebugStringConvertible` protocol and `@DebugDescription` macro come in. In this article, we are taking a look at how to work with this protocol and how to use this new macro in Xcode 16 to make debugging even easier.

### [iOS App Reverse Engineering](https://medium.com/@bellaposa/ios-app-reverse-engineering-de33ab6ca462)

Through reverse engineering, the author of this article was eager to see how much he could tinker with a simple app. He ended up tweaking the pin logic and replaced the usual messages with a playful “Hello World” popup. Hop on to discover how!

## UI

### [Trigger value pattern in SwiftUI](http://swiftwithmajid.com/2024/04/02/trigger-value-pattern-in-swiftui/)

The recent version of the SwiftUI framework introduces a trigger value pattern across its APIs. Trigger value allows us to attach a view modifier that runs its action whenever the trigger value changes. You can find this pattern while using sensory feedback or launching keyframe animation in SwiftUI. Learn how to build custom view modifiers using trigger value pattern with this article.

### [SwiftUI app lifecycle: issues with ScenePhase and using AppDelegate adaptors](https://www.jessesquires.com/blog/2024/06/29/swiftui-scene-phase/)

SwiftUI introduced the `ScenePhase` API in iOS 14 and macOS 11. This was SwiftUI’s answer to handling application lifecycle events. At the same time, SwiftUI introduced `UIApplicationDelegateAdaptor` for iOS and `NSApplicationDelegateAdaptor` for macOS, which allow you to provide an `AppDelegate` on both platforms to receive additional application lifecycle events and other events that were missing from SwiftUI at the time. Unfortunately, many of those application event APIs are still missing and `ScenePhase` has a number of bugs (or at least, unexpected behavior).

## Utils

### [Unobtrusive and testable issue reporting](https://www.pointfree.co/blog/posts/147-unobtrusive-and-testable-issue-reporting)

It is always exciting to check on a new library from Point-Free and this time it's one about Issue Reporting. The library provides tools to report issues in your application and library code as Xcode runtime warnings, breakpoints, assertions, and do so in a testable manner.

### [node-swift](https://swiftpackageindex.com/kabiroberai/node-swift)

From time to time we stumble upon some interesting Swift packages that go beyond what we thought was possible with the language. `node-swift` lets you write native Node modules in Swift that can be used with node.js, NPM and Electron. It's idiomatic, fast, and works on macOS, Linux and Windows.

## Privacy

### [App Tracking Transparency and IDFA on iOS](https://medium.com/@sandeep.kumar.ece16/swift-app-tracking-transparency-and-idfa-on-ios-424cc0668adc)

It's been a while since Apple had introduced some Privacy-related changes with the `AppTrackingFramework` but it was only recently that we saw them requiring apps that open links by using an in-app browser to prompt the user for permission to get tracked. Read on to discover how to integrate this with your app.

### [Meet AccessorySetupKit](https://developer.apple.com/wwdc24/10203)

There's a new framework (iOS 18 and above) that allows you to display a beautiful pairing dialog with an image of your Bluetooth or Wi-Fi accessory — no trip to the Settings app required. Discover how to improve privacy by pairing only your app with an accessory with this WWDC session. And learn how you can migrate existing accessories so they can be managed by `AccessorySetupKit`.
