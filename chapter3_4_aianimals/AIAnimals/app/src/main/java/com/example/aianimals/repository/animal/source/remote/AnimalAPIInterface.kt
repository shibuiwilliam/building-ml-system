package com.example.aianimals.repository.animal.source.remote

import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.*


interface AnimalAPIInterface {
    @Headers("Accept:application/json, Content-Type:application/json")
    @GET("/v0/metadata")
    suspend fun getMetadata(@Header("token") token: String): Response<MetadataResponse>

    @Headers("Accept:application/json, Content-Type:application/json")
    @Multipart
    @POST("/v0/animal")
    suspend fun postAnimal(
        @Header("token") token: String,
        @Part file: MultipartBody.Part,
        @Part json: MultipartBody.Part
    ): Response<List<AnimalResponse>>

    @Headers("Accept:application/json, Content-Type:application/json")
    @POST("/v0/animal/search")
    suspend fun postSearchAnimal(
        @Header("token") token: String,
        @Query("limit") limit: Int = 100,
        @Query("offset") offset: Int = 0,
        @Body post: AnimalSearchPost
    ): Response<AnimalSearchResponse>

    @Headers("Accept:application/json, Content-Type:application/json")
    @POST("/v0/animal/search/similar")
    suspend fun postSearchSimilarAnimal(
        @Header("token") token: String,
        @Body post: SimilarAnimalSearchPost
    ): Response<SimilarAnimalSearchResponse>

    @Headers("Accept:application/json, Content-Type:application/json")
    @GET("/v0/animal")
    suspend fun getAnimal(
        @Header("token") token: String,
        @Query("id") id: String,
        @Query("deactivated") deactivated: Boolean = false,
        @Query("limit") limit: Int = 1,
        @Query("offset") offset: Int = 0,
    ): Response<List<AnimalResponse>>

    @Headers("Accept:application/json, Content-Type:application/json")
    @POST("/v0/like")
    suspend fun postLikeAnimal(
        @Header("token") token: String,
        @Body post: AnimalLikePost
    ): Response<AnimalLikeResponse>
}