import React from 'react'
export default function Footer(){
  return (
    <footer className="footer footer-purple">
      <div className="container grid cols-3">
        <div>
          <h4 className="footer-title">About UniConnect</h4>
          <p className="footer-text">
            UniConnect is a simple learning community for university students to enroll in courses, find mentors,
            form groups, and build real projects together. <strong>Everyone can learn these skills.</strong>
          </p>
        </div>
        <div>
          <h4 className="footer-title">About Me</h4>
          <p className="footer-text">
            I’m <strong>Evans Kaila</strong> — KU CS student and computer programmer. I build practical software
            and teach peers through community-driven learning.
          </p>
        </div>
        <div>
          <h4 className="footer-title">Contact</h4>
          <ul className="footer-list">
            <li>Email: <a href="mailto:evanskaila81@gmail.com">evanskaila81@gmail.com</a></li>
            <li>GitHub: <a href="https://github.com/Polymath-Kaila" target="_blank" rel="noreferrer">Polymath-Kaila</a></li>
            <li>Phone: <a href="tel:0117551826">0117551826</a></li>
          </ul>
        </div>
      </div>
      <div className="container" style={{marginTop:'12px', opacity:0.9}}>
        <small>© {new Date().getFullYear()} UniConnect • Made in Kenya</small>
      </div>
    </footer>
  )
}
