package com.example.aianimals.repository.access_log.source.remote

import com.example.aianimals.repository.BaseRestAPIClient

object AccessAPIClient : BaseRestAPIClient() {
    val gson = provideGson()
    val accessLogAPI: AccessLogAPIInterface =
        getRetrofit(gson).create(AccessLogAPIInterface::class.java)
}