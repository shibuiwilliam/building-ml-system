package com.example.aianimals.services.login

import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class Authenticator
@Inject constructor() {
    fun userLoggedIn() = true
}
