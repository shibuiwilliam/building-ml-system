package com.example.aianimals.repository.animal.source.remote

import com.example.aianimals.repository.BaseRestAPIClient

object AnimalAPIClient: BaseRestAPIClient() {
    val gson = provideGson()
    val animalAPI: AnimalAPIInterface = getRetrofit(gson).create(AnimalAPIInterface::class.java)
}