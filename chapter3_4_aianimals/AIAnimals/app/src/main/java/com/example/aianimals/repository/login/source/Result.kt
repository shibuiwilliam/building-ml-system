package com.example.aianimals.repository.login.source

import com.example.aianimals.repository.login.Login

sealed class Result<out T : Login> {
    data class Success<out T : Login>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()

    override fun toString(): String {
        return when (this) {
            is Success<*> -> "Success[data=$data]"
            is Error -> "Error[exception=$exception]"
        }
    }

    fun getLogin(): Login? {
        return when (this) {
            is Success<*> -> data
            is Error -> null
        }
    }
}
