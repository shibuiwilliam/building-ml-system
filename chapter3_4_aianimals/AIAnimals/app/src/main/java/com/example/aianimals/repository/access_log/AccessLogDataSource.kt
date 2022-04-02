package com.example.aianimals.repository.access_log.source

import com.example.aianimals.repository.access_log.AccessLog

interface AccessLogDataSource {
    suspend fun createAccessLog(accessLog: AccessLog)
}