package com.example.aianimals.repository.login.source.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.example.aianimals.middleware.Converters
import com.example.aianimals.repository.login.Login

@Database(
    entities = [Login::class],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class LoginDatabase : RoomDatabase() {
    abstract fun loginDao(): LoginDao

    companion object {
        private var INSTANCE: LoginDatabase? = null
        private val lock = Any()

        fun getInstance(context: Context): LoginDatabase {
            synchronized(LoginDatabase.lock) {
                if (LoginDatabase.INSTANCE == null) {
                    LoginDatabase.INSTANCE = Room.databaseBuilder(
                        context.applicationContext,
                        LoginDatabase::class.java,
                        "Logins.db"
                    )
                        .fallbackToDestructiveMigration()
                        .build()
                }
                return LoginDatabase.INSTANCE!!
            }
        }
    }
}