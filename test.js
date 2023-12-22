<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <link rel="stylesheet" href="style.css" />

    <style>
      body {
        background: #000;
        color: white;
      }

      @keyframes soundwaveBar {
        0% {
          height: 0;
        }
        50% {
          height: 40%;
        }
        100% {
          height: 0;
        }
      }

      .soundwave-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        height: 300px;

        .bar {
          margin-left: 1px;
          margin-right: 2px;
          width: 2px;
          height: 0;
          background: skyblue;
          line-height: normal;
          vertical-align: middle;
          animation-name: soundwaveBar;
          animation-iteration-count: infinite;
          will-change: height;
        }
      }

      button {
        padding: 7px 20px;
        cursor: pointer;
      }

      p {
        color: white;
      }

      main {
        text-align: center;
      }

      .voiceplayer {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 30px;
      }

      a {
        display: block;
        /* Change to display none after testing */
        display: none;
      }
    </style>
  </head>
  <body>
    <main>
      <div id="soundwave" class="soundwave-wrap"></div>
      <!--  -->
      <div class="voiceplayer">
        <div class="btn-wrapper">
          <button id="startRecording">Start</button>
          <button id="stopRecording">Stop</button>
        </div>
        <br />
        <p id="isRecording">Click start button to record</p>
        <audio src="" id="audioElement" autoplay controls></audio>
      </div>
      <!-- Empty div to store the recorded files, This is the element you asked for -->
      <div id="recordingsContainer"></div>
    </main>

    <!-- Script -->
    <script>
      // Incrementing ID
      let recIndex = 0;

      document
        .getElementById("startRecording")
        .addEventListener("click", initFunction);
      let isRecording = document.getElementById("isRecording");

      function initFunction() {
        // Display recording
        async function getUserMedia(constraints) {
          if (window.navigator.mediaDevices) {
            return window.navigator.mediaDevices.getUserMedia(constraints);
          }
          let legacyApi =
            navigator.getUserMedia ||
            navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia ||
            navigator.msGetUserMedia;
          if (legacyApi) {
            return new Promise(function (resolve, reject) {
              legacyApi.bind(window.navigator)(constraints, resolve, reject);
            });
          } else {
            alert("user api not supported");
          }
        }
        isRecording.textContent = "Recording...";

        //recording variables
        let audioChunks = [];
        let record;

        function handlerFunction(stream) {
          record = new MediaRecorder(stream);

          record.start();

          record.ondataavailable = (e) => {
            audioChunks.push(e.data);

            if (record.state == "inactive") {
              let blob = new Blob(audioChunks, { type: "audio/mp3" });
              console.log(blob);

              const audioElement = document.getElementById("audioElement");
              audioElement.src = URL.createObjectURL(blob);

              // Create a byte from the record
              let reader = new FileReader();

              reader.onloadend = () => {
                // Get the raw binary data (ArrayBuffer)
                let arrayBuffer = reader.result;

                // Access the raw bytes as a Uint8Array
                let byteArray = new Uint8Array(arrayBuffer);

                console.log(byteArray);
              };

              reader.readAsArrayBuffer(blob);

              // Create a download link for the recorded audio
              const downloadLink = document.createElement("a");
              downloadLink.href = audioElement.src;
              // audio recording now contained in the downloadLink.href above
              downloadLink.download = `recording_${recIndex}.mp3`;
              downloadLink.textContent = `Download Recording ${recIndex}`;

              // recIndex++;

              // Append the audio element and download link to an empty container
              const recordingsContainer = document.getElementById(
                "recordingsContainer"
              );
              recordingsContainer.appendChild(audioElement);
              recordingsContainer.appendChild(downloadLink);

              // so after the recordings have been made, you can get the recorded item using python by targetting the
            }
          };
        }

        function startusingBrowserMicrophone(boolean) {
          getUserMedia({ audio: boolean }).then((stream) => {
            handlerFunction(stream);
          });
        }
        startusingBrowserMicrophone(true);
        // Stoping handler
        document
          .getElementById("stopRecording")
          .addEventListener("click", (e) => {
            record.stop();
            isRecording.textContent = "Click play button to start listening";
          });
      }
    </script>
  </body>
</html>