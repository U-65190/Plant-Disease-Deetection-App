package com.animegamer.myapplication;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import okhttp3.Callback;
import okhttp3.RequestBody;
import okhttp3.MultipartBody;
import okhttp3.MediaType;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.scalars.ScalarsConverterFactory;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;




public class MainActivity extends AppCompatActivity {

    private static final int PICK_IMAGE_REQUEST = 1;

    private ImageView imagePreview;
    private Spinner cropSpinner;
    private Button btnSubmit;
    private TextView outputText;

    private Uri imageUri;
    private String[] crops = {"apple", "cherry", "corn", "grape"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imagePreview = findViewById(R.id.imagePreview);
        cropSpinner = findViewById(R.id.cropSpinner);
        btnSubmit = findViewById(R.id.btnSubmit);
        outputText = findViewById(R.id.outputText);

        // Setup dropdown
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, crops);
        cropSpinner.setAdapter(adapter);

        // Click on image to select
        imagePreview.setOnClickListener(v -> openFileChooser());

        // Submit logic
        btnSubmit.setOnClickListener(v -> {
            if (imageUri != null) {
                uploadToServer();
            } else {
                Toast.makeText(this, "Please select an image.", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void openFileChooser() {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("image/*");
        startActivityForResult(intent, PICK_IMAGE_REQUEST);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == PICK_IMAGE_REQUEST && resultCode == RESULT_OK && data != null && data.getData() != null) {
            imageUri = data.getData();
            imagePreview.setImageURI(imageUri);
        }
    }

    private void uploadToServer() {
        String crop = cropSpinner.getSelectedItem().toString();
        File imageFile;

        try {
            InputStream inputStream = getContentResolver().openInputStream(imageUri);
            imageFile = new File(getCacheDir(), "input.jpg");
            OutputStream outputStream = new FileOutputStream(imageFile);
            byte[] buffer = new byte[1024];
            int length;
            while ((length = inputStream.read(buffer)) > 0) {
                outputStream.write(buffer, 0, length);
            }
            outputStream.close();
            inputStream.close();
        } catch (Exception e) {
            outputText.setText("Image read error: " + e.getMessage());
            return;
        }

        RequestBody cropPart = RequestBody.create(crop, MediaType.parse("text/plain"));
        RequestBody filePart = RequestBody.create(imageFile, MediaType.parse("image/*"));
        MultipartBody.Part imageBody = MultipartBody.Part.createFormData("image", "input.jpg", filePart);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://YOUR_SERVER_IP:8000/") // <- Change this!
                .addConverterFactory(ScalarsConverterFactory.create())
                .build();

        ApiService api = retrofit.create(ApiService.class);
        Call<String> call = api.uploadImage(imageBody, cropPart);

        call.enqueue(new retrofit2.Callback<String>() {
            @Override
            public void onResponse(Call<String> call, Response<String> response) {
                if (response.isSuccessful()) {
                    outputText.setText(response.body());
                } else {
                    outputText.setText("Response error: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<String> call, Throwable t) {
                // Handle failure here
                outputText.setText("Error: " + t.getMessage());
            }
        });
    }
}
