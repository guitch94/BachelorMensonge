package com.example.camgame

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.graphics.Matrix
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.util.Size
import android.view.Surface
import android.view.TextureView
import android.view.ViewGroup
import android.widget.*
import androidx.camera.core.*
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleOwner
import kotlinx.android.synthetic.main.activity_video.*
import java.io.File
import java.lang.Exception
import java.util.concurrent.Executors


private const val REQUEST_CODE_PERMISSIONS = 10

private val REQUIRED_PERMISSIONS = arrayOf(Manifest.permission.CAMERA, Manifest.permission.RECORD_AUDIO)
private val tag = MainActivity::class.java.simpleName

@SuppressLint("RestrictedApi")
class Video : AppCompatActivity() {

    private val lensFacing = CameraX.LensFacing.FRONT
    private val executor = Executors.newSingleThreadExecutor()
    private lateinit var viewFinder: TextureView // affichage de la prévisualisation de la caméra
    private lateinit var viewVideo : VideoView // affichage de la vidéo à décrire
    private lateinit var viewRect : ImageView // affichage du rectangle aidant à centrer la personne
    private var randVideo = 0
    private var lieOrTruth = ""
    private var mode = "" // mode normal, émotion ou choquant

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_video)

        // initialisation des affichages
        viewFinder = findViewById<TextureView>(R.id.view_finder)
        viewVideo =  findViewById<VideoView>(R.id.videoView)
        viewRect =  findViewById<ImageView>(R.id.image_view)
        mode = intent.getStringExtra("mode") // récupération du mode choisi par l'utilisateur

        viewRect.setImageResource(R.drawable.rect3) // affichage du rectangle


        randVideo = (1..6).random()

        if((1..2).random() == 1)
            lieOrTruth = "Mensonge"
        else
            lieOrTruth = "Vérité"

        // recherche et affichage de la vidéo en fonction du nombre aléatoire et du mode
        val uri = Uri.parse("android.resource://" + getPackageName() + "/" + getResources().getIdentifier(mode + randVideo,
            "raw", getPackageName()))
        Log.d("URI", uri.toString() + "num" + randVideo)
        videoView.setVideoURI(uri)

        // Demande des permissions pour la caméra
        if (allPermissionsGranted()) {
            viewFinder.post { startCamera() }
        } else {
            ActivityCompat.requestPermissions(
                this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS)
        }

        // Pour chaque changement de la prévisualisation, on recalcul la disposition
        viewFinder.addOnLayoutChangeListener { _, _, _, _, _, _, _, _, _ ->
            updateTransform()
        }
    }



    @SuppressLint("RestrictedApi")
    private fun startCamera() {

        // Configuration de la prévisualisation
        val previewConfig = PreviewConfig.Builder().apply {
            setLensFacing(lensFacing)
            setTargetResolution(Size(640, 500))
        }.build()


        val preview = Preview(previewConfig)

        // Pour chaque mise à jour de la prévisualisation, on recalcul la disposition
        preview.setOnPreviewOutputUpdateListener {

                        val parent = viewFinder.parent as ViewGroup
            parent.removeView(viewFinder)
            parent.addView(viewFinder, 0)

            viewFinder.surfaceTexture = it.surfaceTexture
            updateTransform()
        }
        // Configuration de la capture vidéo
        val videoCaptureConfig = VideoCaptureConfig.Builder().apply {
            setLensFacing(lensFacing) // utilisation de la caméra frontale
            setTargetRotation(viewFinder.display.rotation)
            //setVideoFrameRate(30) // Doit forcer le nombre de fps
        }.build()

        val videoCapture = VideoCapture(videoCaptureConfig)

        val button =  findViewById<Button>(R.id.videoButton)
        var firstTimeClick = true

        button.setOnClickListener {
            if(firstTimeClick == true) {

                val file = File(externalMediaDirs.first(), lieOrTruth + "_" + mode +"_"+ randVideo.toString() + "_" + "${System.currentTimeMillis()}.mp4")
                firstTimeClick = false
                button.setText("stop") // change le bouton start en bouton stop
                viewVideo.start()
                viewVideo.resume()

                // indique si l'utilisateur doit mentir ou dire la vérité
                Toast.makeText(applicationContext, lieOrTruth, Toast.LENGTH_SHORT).show()

                videoCapture.startRecording(
                    file,
                    executor,
                    object : VideoCapture.OnVideoSavedListener {
                        override fun onVideoSaved(file: File) {
                            val msg = "Video saved in ${file.absolutePath}"
                            Log.d("CameraXDemo", msg)
                        }

                        override fun onError(
                            videoCaptureError: VideoCapture.VideoCaptureError,
                            message: String,
                            cause: Throwable?
                        ) {

                            val msg = "Video capture failed: $message"
                            Toast.makeText(applicationContext, msg, Toast.LENGTH_SHORT).show()
                            Log.e("CameraXApp", msg)
                            cause?.printStackTrace()
                        }
                    })
            }else{
                videoCapture.stopRecording()
                viewVideo.suspend()
                firstTimeClick = true
                Toast.makeText(applicationContext, "MERCI", Toast.LENGTH_SHORT).show()
                finish()
            }
        }


        // On relie les cas d'utilisation de prévisualisation et de capture de vidéos au cycle
        // de vie de l'application
        CameraX.bindToLifecycle(this, preview, videoCapture)

    }

    private fun updateTransform() {
        val matrix = Matrix()

        // Calcul du centre de la texture view
        val centerX = viewFinder.width / 2f
        val centerY = viewFinder.height / 2f

        // Correction de la sortie d'affichage en tenant compte de la rotation
        val rotationDegrees = when(viewFinder.display.rotation) {
            Surface.ROTATION_0 -> 0
            Surface.ROTATION_90 -> 90
            Surface.ROTATION_180 -> 180
            Surface.ROTATION_270 -> 270
            else -> return
        }
        matrix.postRotate(-rotationDegrees.toFloat(), centerX, centerY)

        // Applique la transformation à notre textureView
        viewFinder.setTransform(matrix)
    }

    /**
     * On traite le résultat de la boite de dialogue de demande d'autorisation.
     * Si toutes les autorisations ont été accordées, on lance la caméra sinon
     * on affiche un Toast (Pop-up android)
     */
    override fun onRequestPermissionsResult(
        requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            if (allPermissionsGranted()) {
                viewFinder.post { startCamera() }
            } else {
                Toast.makeText(this,
                    "Permissions not granted by the user.",
                    Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    /**
     * vérifie si toutes les permissions du manifeste ont été accordées
     */
    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
        ContextCompat.checkSelfPermission(
            baseContext, it) == PackageManager.PERMISSION_GRANTED
    }
}


