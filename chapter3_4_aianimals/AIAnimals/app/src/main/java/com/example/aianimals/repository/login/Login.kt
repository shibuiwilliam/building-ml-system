package com.example.aianimals.repository.login

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.*

@Entity(tableName = "logins")
data class Login @JvmOverloads constructor(
    @PrimaryKey @ColumnInfo(name = "id") val id: Int = 0,
    @ColumnInfo(name = "userID") val userID: String,
    @ColumnInfo(name = "handleName") val handleName: String,
    @ColumnInfo(name = "emailAddress") val emailAddress: String,
    @ColumnInfo(name = "token") val token: String?,
    @ColumnInfo(name = "lastLoginAt") val lastLoginAt: Date
)