---
title: "Why Does Passing NSManagedObjectContext Across Isolation Domains No Longer Error in Swift 6.2? The Real Change Isn't in the Compiler"
url: "https://fatbobman.com/en/posts/sendable-nsmanagedobjectcontext/"
author_name: "Xu Yang"
author_url: "https://bsky.app/profile/fatbobman.com"
section: "Concurrency"
tags: ["NSManagedObjectContext", "Swift Concurrency"]
description: "`NSManagedObjectContext` suddenly compiles across isolation domains in Swift 6.2—but the compiler hasn't changed. The real answer lies in SDK annotations, not language evolution."
published_date: "2026-03-04"
---
<!-- SECTION: Concurrency -->

### [Why Does Passing NSManagedObjectContext Across Isolation Domains No Longer Error in Swift 6.2? The Real Change Isn't in the Compiler](https://fatbobman.com/en/posts/sendable-nsmanagedobjectcontext/)

[Xu Yang](https://bsky.app/profile/fatbobman.com)

`NSManagedObjectContext` suddenly compiles across isolation domains in Swift 6.2—but the compiler hasn't changed. The real answer lies in SDK annotations, not language evolution.
