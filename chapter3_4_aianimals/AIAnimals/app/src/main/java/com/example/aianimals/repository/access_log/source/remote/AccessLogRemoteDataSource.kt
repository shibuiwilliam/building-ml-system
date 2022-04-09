package com.example.aianimals.repository.access_log.source.remote

import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.access_log.AccessLog
import com.example.aianimals.repository.access_log.source.AccessLogDataSource
import kotlinx.coroutines.withContext

class AccessLogRemoteDataSource private constructor(
    val appExecutors: AppExecutors,
    val accessLogAPI: AccessLogAPIInterface
) : AccessLogDataSource {
    private val TAG = AccessLogRemoteDataSource::class.java.simpleName

    private var token: String? = null
    private var userID: String? = null

    override suspend fun createAccessLog(accessLog: AccessLog) {
        if (token == null) {
            return
        }
        withContext(appExecutors.ioContext) {
            accessLogAPI.postAccessLog(
                token!!,
                AccessLogPost(
                    accessLog.phrases,
                    accessLog.animalCategoryID,
                    accessLog.animalSubcategoryID,
                    accessLog.animalID,
                    accessLog.action
                )
            )
        }
    }
}