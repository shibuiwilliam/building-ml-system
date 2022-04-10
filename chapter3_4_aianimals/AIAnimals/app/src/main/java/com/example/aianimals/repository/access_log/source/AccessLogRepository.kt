package com.example.aianimals.repository.access_log.source

import com.example.aianimals.repository.access_log.AccessLog
import com.example.aianimals.repository.access_log.source.local.AccessLogLocalDataSource
import com.example.aianimals.repository.access_log.source.remote.AccessLogRemoteDataSource

class AccessLogRepository(
    val accessLogLogDataSource: AccessLogLocalDataSource,
    val accessLogRemoteDataSource: AccessLogRemoteDataSource
) : AccessLogDataSource {
    private val TAG = AccessLogRepository::class.java.simpleName

    override suspend fun createAccessLog(accessLog: AccessLog) {
        accessLogRemoteDataSource.createAccessLog(accessLog)
    }

    companion object {
        private var INSTANCE: AccessLogRepository? = null

        @JvmStatic
        fun getInstance(
            accessLogLogDataSource: AccessLogLocalDataSource,
            accessLogRemoteDataSource: AccessLogRemoteDataSource
        ): AccessLogRepository {
            return INSTANCE ?: AccessLogRepository(
                accessLogLogDataSource,
                accessLogRemoteDataSource
            ).apply { INSTANCE = this }
        }

        @JvmStatic
        fun destroyInstance() {
            INSTANCE = null
        }
    }
}