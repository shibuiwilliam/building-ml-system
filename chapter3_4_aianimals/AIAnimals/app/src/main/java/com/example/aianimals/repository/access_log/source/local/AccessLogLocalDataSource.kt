package com.example.aianimals.repository.access_log.source.local

import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.access_log.AccessLog
import com.example.aianimals.repository.access_log.source.AccessLogDataSource

class AccessLogLocalDataSource private constructor(
    val appExecutors: AppExecutors
) : AccessLogDataSource {
    private val TAG = AccessLogLocalDataSource::class.java.simpleName

    override suspend fun createAccessLog(accessLog: AccessLog) {
        TODO("Not yet implemented")
    }
}