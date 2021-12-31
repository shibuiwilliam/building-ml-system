package com.example.aianimals.repository.login.source.remote

import com.example.aianimals.repository.BaseRestAPIClient

object LoginAPIClient: BaseRestAPIClient() {
    val gson = provideGson()
    val loginAPI: LoginAPIInterface = getRetrofit(gson).create(LoginAPIInterface::class.java)
}