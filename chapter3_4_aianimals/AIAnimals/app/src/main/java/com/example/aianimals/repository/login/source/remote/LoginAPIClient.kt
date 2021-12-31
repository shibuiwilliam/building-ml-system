package com.example.aianimals.repository.login.source.remote

import com.example.aianimals.repository.BaseRestAPIClient

object LoginAPIClient: BaseRestAPIClient() {
    val gson = provideGson()
    val loginAPIInterface: LoginAPIInterface = getRetrofit(gson).create(LoginAPIInterface::class.java)
}