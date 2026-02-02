---
title: "isolated(any) and #isolation: Letting Swift Closures Automatically Inherit Isolation"
external_url: "https://fatbobman.com/en/posts/letting-swift-closures-automatically-inherit-isolation/"
author_name: "Xu Yang"
author_link: "https://bsky.app/profile/fatbobman.com"
section: "Concurrency"
tags: ['Swift', 'Actors', 'AI']
description: "Swift 6's `@isolated(any)` and `#isolation` macro eliminate manual `@MainActor` annotations by teaching closures to automatically inherit their execution context."
published_date: "2026-01-21"
---
<!-- SECTION: Concurrency -->

### [isolated(any) and #isolation: Letting Swift Closures Automatically Inherit Isolation](https://fatbobman.com/en/posts/letting-swift-closures-automatically-inherit-isolation/)

[Xu Yang](https://bsky.app/profile/fatbobman.com)

Swift 6's `@isolated(any)` and `#isolation` macro eliminate manual `@MainActor` annotations by teaching closures to automatically inherit their execution context.
