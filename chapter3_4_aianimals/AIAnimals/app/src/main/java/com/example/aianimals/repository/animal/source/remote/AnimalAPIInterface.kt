package com.example.aianimals.repository.animal.source.remote

import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Headers
import retrofit2.http.POST

interface AnimalAPIInterface {
    @Headers("Accept:application/json, Content-Type:application/json")
    @GET("/v0/metadata")
    suspend fun getMetadata(@Header("token") token: String): Response<MetadataResponse>
}