package com.example.aianimals.middleware

import kotlinx.coroutines.Dispatchers
import kotlin.coroutines.CoroutineContext

open class AppExecutors constructor(
    val ioContext: CoroutineContext = Dispatchers.IO,
    val defaultContext: CoroutineContext = Dispatchers.Default,
)