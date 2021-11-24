package com.example.aianimals.services.animal.listing

import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path

internal interface AnimalsApi {
    companion object {
        private const val PARAM_ANIMAL_ID = "animalId"
        private const val ANIMALS = "animals.json"
        private const val ANIMAL_DETAILS = "animal_0{$PARAM_ANIMAL_ID}.json"
    }

    @GET(ANIMALS)
    fun animals(): Call<List<AnimalEntity>>
    @GET(ANIMAL_DETAILS)
    fun animalDetails(@Path(PARAM_ANIMAL_ID) animalId: Int): Call<AnimalDetailsEntity>
}
