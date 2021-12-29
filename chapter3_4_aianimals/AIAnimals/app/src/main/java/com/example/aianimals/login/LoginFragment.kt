package com.example.aianimals.login

import android.content.Intent
import android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.lifecycle.Observer
import com.example.aianimals.R
import com.example.aianimals.listing.listing.AnimalListActivity


class LoginFragment : Fragment(), LoginContract.View {
    private val TAG = LoginFragment::class.java.simpleName

    override lateinit var presenter: LoginContract.Presenter

    private lateinit var loginText: TextView
    private lateinit var idEdit: EditText
    private lateinit var passwordEdit: EditText
    private lateinit var loginButton: Button

    override fun show(){
        loginText.visibility = View.VISIBLE
        idEdit.visibility = View.VISIBLE
        passwordEdit.visibility = View.VISIBLE
        loginButton.visibility = View.VISIBLE
    }

    override fun login() {
        presenter.login(idEdit.text.toString(), passwordEdit.text.toString())
    }

    override fun onResume() {
        super.onResume()
        presenter.start()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(R.layout.login_fragment, container, false)

        with(root){
            activity?.title = getString(R.string.login)

            loginText=findViewById(R.id.login_text)
            idEdit=findViewById(R.id.id_edit)
            passwordEdit=findViewById(R.id.password_edit)
            loginButton=findViewById(R.id.login_button)

            presenter.loginResult.observe(this@LoginFragment, Observer {
                val loginResult = it ?: return@Observer

                if(loginResult.error != null) {
                    Toast.makeText(requireContext(), "login failed", Toast.LENGTH_SHORT).show()
                }
                if (loginResult.success != null) {
                    val intent = Intent(context, AnimalListActivity::class.java)
                    intent.flags = FLAG_ACTIVITY_CLEAR_TASK or Intent.FLAG_ACTIVITY_NEW_TASK
                    startActivity(intent)
                }
            })

            loginButton.setOnClickListener {
                login()
            }
        }
        return root
    }

    companion object {
        fun newInstance() = LoginFragment()
    }
}