document.getElementById('searchVideosBtn').addEventListener('click', function() {
    const subject = document.getElementById('subjectFilter').value.toLowerCase();
    const year = document.getElementById('yearFilter').value.toLowerCase();
    const course = document.getElementById('courseFilter').value.toLowerCase();

    filterVideos(subject, year, course);
});

function filterVideos(subject, year, course) {
    const videos = document.querySelectorAll('.video');
    
    videos.forEach(video => {
        const videoSubject = video.getAttribute('data-subject').toLowerCase();
        const videoYear = video.getAttribute('data-year').toLowerCase();
        const videoCourse = video.getAttribute('data-course').toLowerCase();
        
        if ((subject === "" || videoSubject.includes(subject)) &&
            (year === "" || videoYear.includes(year)) &&
            (course === "" || videoCourse.includes(course))) {
            video.style.display = 'block';
        } else {
            video.style.display = 'none';
        }
    });
}