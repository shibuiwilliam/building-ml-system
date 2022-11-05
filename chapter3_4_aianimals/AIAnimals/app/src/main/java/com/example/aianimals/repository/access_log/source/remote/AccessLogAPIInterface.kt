package com.example.aianimals.repository.access_log.source.remote

import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.Headers
import retrofit2.http.POST

interface AccessLogAPIInterface {
    @Headers("Accept:application/json, Content-Type:application/json")
    @POST("/v0/access_log")
    suspend fun postAccessLog(
        @Header("token") token: String,
        @Body post: AccessLogPost
    )
}