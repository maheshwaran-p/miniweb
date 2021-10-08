

Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('/static'),
    faceapi.nets.faceLandmark68Net.loadFromUri('/static'),
    faceapi.nets.faceRecognitionNet.loadFromUri('/static'),
    faceapi.nets.faceExpressionNet.loadFromUri('/static')
]).then(startVideo)

function startVideo() {
    const video = document.getElementById('video')
    console.log("startVIDEO");
    navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    navigator.getMedia({
        video: true,
        audio: false
    }, function (stream) {
        video.srcObject = stream;
        video.play();
    }, function (error) {
        //error.code
    }
    );



    console.log("video event listener")
    const canvas = faceapi.createCanvasFromMedia(video)
    document.body.append(canvas)
    const displaySize = { width: video.width, height: video.height }
    faceapi.matchDimensions(canvas, displaySize)
    setInterval(async () => {
        const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
        const resizedDetections = faceapi.resizeResults(detections, displaySize)
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
        faceapi.draw.drawDetections(canvas, resizedDetections)
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
        faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
    }, 100)





    // navigator.getMedia(
    //     { video: {} },
    //     stream => video.srcObject = stream,
    //     err => console.error(err)
    // )
}
startVideo()

video.addEventListener('playing', () => {
    console.log("video event listener")
    const canvas = faceapi.createCanvasFromMedia(video)
    document.body.append(canvas)
    const displaySize = { width: video.width, height: video.height }
    faceapi.matchDimensions(canvas, displaySize)
    setInterval(async () => {
        const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
        const resizedDetections = faceapi.resizeResults(detections, displaySize)
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
        faceapi.draw.drawDetections(canvas, resizedDetections)
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
        faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
    }, 100)
})

