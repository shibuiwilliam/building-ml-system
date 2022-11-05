package com.example.aianimals.repository.login.source.remote

import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST

interface LoginAPIInterface {
    @Headers("Accept:application/json, Content-Type:application/json")
    @POST("/v0/user/login")
    suspend fun postLogin(@Body post: LoginPost): Response<LoginResponse>
}