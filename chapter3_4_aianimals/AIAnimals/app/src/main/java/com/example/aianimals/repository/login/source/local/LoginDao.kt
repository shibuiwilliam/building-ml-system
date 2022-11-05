package com.example.aianimals.repository.login.source.local

import androidx.room.*
import com.example.aianimals.repository.login.Login

@Dao
interface LoginDao {
    @Query("SELECT * FROM logins WHERE id = :id")
    fun getLogin(id: Int = 0): Login?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertLogin(login: Login)

    @Delete
    fun deleteLogin(login: Login)
}