package com.example.aianimals.middleware

import android.os.Handler
import android.os.Looper
import java.util.concurrent.Executor
import java.util.concurrent.Executors

const val THREAD_COUNT = 4

open class AppExecutors constructor(
    val diskIO: Executor = DiskIOThreadExecutor(),
    val networkIO: Executor = Executors.newFixedThreadPool(THREAD_COUNT),
    val mainThread: Executor = MainThreadExecutor()
) {

    private class MainThreadExecutor : Executor {
        private val mainThreadHandler = Handler(Looper.getMainLooper())

        override fun execute(command: Runnable) {
            mainThreadHandler.post(command)
        }
    }
}