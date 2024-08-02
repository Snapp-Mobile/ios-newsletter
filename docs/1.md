---
layout: default
title: Snapp Mobile iOS Newsletter 1
issue: 1
date: 2024-08-02
---
## Swift

### [Announcing Swift Homomorphic Encryption](https://www.swift.org/blog/announcing-swift-homomorphic-encryption/)

Homomorphic encryption (HE) is a cryptographic technique that enables computation on encrypted data without revealing the underlying unencrypted data to the operating process. It provides a means for clients to send encrypted data to a server, which operates on that encrypted data and returns a result that the client can decrypt. During the execution of the request, the server itself never decrypts the original data or even has access to the decryption key. Such an approach presents new opportunities for cloud services to operate while protecting the privacy and security of a user's data, which is obviously highly attractive for many scenarios.

### [Swift-foundation now available as part of the nightly toolchains for Swift 6.0](https://forums.swift.org/t/swift-foundation-now-available/73530)

As part of the commitment to investing in Swift across all platforms, the Swift core team had just announced the availability of the new all-Swift Foundation library as part of the Swift 6 nightly toolchain, supporting Linux and Windows. 🏗️🏗️🏗️ 

Even better - no adoption is required. If you import `Foundation` on Linux or Windows today, you will be using the new implementation. You can now also use `FoundationEssentials` or `FoundationInternationalization` to get a focused subset of the complete Foundation API.

### [Updated App Review Guidelines guidelines now available](https://developer.apple.com/news/?id=ty0avr2s)

The App Review Guidelines have been revised to support updated policies and upcoming features, and to provide clarification.

### [Trigger property observers from initializers in Swift](https://nilcoalescing.com/blog/TriggerPropertyObserversFromInitializersInSwift/)

In Swift, property observers such as `willSet` and `didSet` are not called when a property is set in an initializer. This is by design, as the initializer's purpose is to set up the initial state of an object, and during this phase, the object is not yet fully initialized. However, if we need to perform some actions similar to what we'd do in property observers during initialization, there are some workarounds as [Natalia Panferova](https://x.com/natpanferova) discovers

### [Advanced Async Sequences in Swift](https://swiftonserver.com/advanced-async-sequences/)

`AsyncSequence`s are very prevalent in Swift, and are becoming more prominent in macOS and iOS apps as well. Like other structured concurrency features, `AsyncSequence`s enable structured programming. This makes it easier for you to reason about your code, and write more robust code free of data races.

## UI

### [Navigation patterns in SwiftUI](https://azamsharp.com/2024/07/29/navigation-patterns-in-swiftui.html)

Navigation has often been a challenge in SwiftUI applications. Initially, SwiftUI introduced `NavigationView`, which was later replaced by `NavigationStack` in iOS 16.

`NavigationStack` enhanced navigation by enabling dynamic and programmatic routing, and it also offered ways to centralize routes for the entire application. In this article, Mohammad Azam explores some common navigation patterns that can be employed when building SwiftUI applications.

### [Demystify SwiftUI containers](https://developer.apple.com/wwdc24/10146)

This session form the WWDC 2024 teaches us about the capabilities of SwiftUI container views and helps us build a mental model for how subviews are managed by their containers. Learn how to leverage new APIs to build your own custom containers, create modifiers to customize container content, and give your containers that extra polish that helps your apps stand out.

## Xcode tips

### [Paste in Xcode's navigator area to create a file](https://x.com/v_pradeilles/status/1818610834232508534)

[Vincent Pradeilles](https://x.com/v_pradeilles) shared a cool new feature available on Xcode 16. You can now paste content into the Project Navigator, and Xcode will automatically create a new file with the approriate name. Neat!
