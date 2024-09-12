const notes = [
  {
    id: 1,
    subject: "Mathematics",
    year: "1st Year",
    title: "Differential Calculus 1",
    description:
      "Notes of Differential Calculus 1 for 1st or 2nd semester students",
    pdfLink: "math/mth2.pdf",
  },
  {
    id: 2,
    subject: "Physics",
    year: "1st Year",
    title: "Quantum Physics",
    description: "Notes on Quantum Physics for 1st or 2nd semester students",
    pdfLink: "physic/phy1.pdf",
  },
  {
    id: 3,
    subject: "Chemistry",
    year: "1st Year",
    title: "UNIT 1 Notes",
    description: "Notes on Organic Chemistry for 1st or 2nd semester students",
    pdfLink: "chemistry/che1.pdf",
  },
  {
    id: 4,
    subject: "Programing for Problem Solving",
    year: "1st Year",
    title: "UNIT 1 Notes",
    description: "Notes on Data Structures for 2nd semester students",
    pdfLink: "pps/pps1.pdf",
  },
  {
    id: 5,
    subject: "Electrical Engineering",
    year: "1st Year",
    title: "UNIT-1",
    description: "Notes on UNIT-1 for 1st or 2nd semester students",
    pdfLink: "BEE/ee1.pdf",
  },
  {
    id: 6,
    subject: "Mechanical Engineering",
    year: "1st Year",
    title: "Introduction mechanics",
    description: "Notes on Thermodynamics for 5th semester students",
    pdfLink: "machanical/me1.pdf",
  },
  {
    id: 7,
    subject: "Mechanical Engineering",
    year: "1st Year",
    title: "Ic engine and Evs",
    description: "Notes on IC engine And EVS for 1st or 2nd semester students",
    pdfLink: "machanical/me2.pdf",
  },
  {
    id: 8,
    subject: "Mathematics",
    year: "1st Year",
    title: "Matrix",
    description: "Notes on Matrix for 1st or 2nd semester students",
    pdfLink: "math/mth1.pdf",
  },
  {
    id: 9,
    subject: "Mathematics",
    year: "1st Year",
    title: "Differential Calculus 2",
    description:
      "Notes on Differential Calculus 2 for 1st or 2nd semester students",
    pdfLink: "math/mth2.pdf",
  },
  {
    id: 10,
    subject: "Mathematics",
    year: "1st Year",
    title: "Integral Calculus 1",
    description:
      "Notes on Integral Calculus 1 for 1st or 2nd semester students",
    pdfLink: "math/mth4.pdf",
  },
  {
    id: 11,
    subject: "Mathematics",
    year: "1st Year",
    title: "Integral Calculus 2",
    description:
      "Notes on Integral Calculus 2 for 1st or 2nd semester students",
    pdfLink: "math/mth5.pdf",
  },
  {
    id: 12,
    subject: "Physics",
    year: "1st Year",
    title: "Electromagnetic Field Theory",
    description:
      "Notes on Electromagnetic Field Theory for 1st or 2nd semester students",
    pdfLink: "physic/phy2.pdf",
  },
  {
    id: 13,
    subject: "Physics",
    year: "1st Year",
    title: "Wave Optics",
    description: "Notes on Wave Optics for 1st or 2nd semester students",
    pdfLink: "physic/phy3.pdf",
  },
  {
    id: 14,
    subject: "Physics",
    year: "1st Year",
    title: "Fibre Optics and Laser",
    description:
      "Notes on Fibre Optics and Laser for 1st or 2nd semester students",
    pdfLink: "physic/phy4.pdf",
  },
  {
    id: 15,
    subject: "Physics",
    year: "1st Year",
    title: "Superconductor and Nano Materials",
    description:
      "Notes on Superconductor and Nano Materials for 1st or 2nd semester students",
    pdfLink: "physic/phy5.pdf",
  },
  {
    id: 16,
    subject: "Chemistry",
    year: "1st Year",
    title: "UNIT 2 Notes",
    description: "Notes on Organic Chemistry for 1st or 2nd semester students",
    pdfLink: "chemistry/che2.pdf",
  },
  {
    id: 17,
    subject: "Chemistry",
    year: "1st Year",
    title: "UNIT 3 Notes",
    description: "Notes on Organic Chemistry for 1st or 2nd semester students",
    pdfLink: "chemistry/che3.pdf",
  },
  {
    id: 18,
    subject: "Chemistry",
    year: "1st Year",
    title: "UNIT 4 Notes",
    description: "Notes on Organic Chemistry for 1st or 2nd semester students",
    pdfLink: "chemistry/che4.pdf",
  },
  {
    id: 19,
    subject: "Chemistry",
    year: "1st Year",
    title: "UNIT 5 Notes",
    description: "Notes on Organic Chemistry for 1st or 2nd semester students",
    pdfLink: "chemistry/che5.pdf",
  },
  {
    id: 20,
    subject: "Mechanical Engineering",
    year: "1st Year",
    title: "Refrigeration and AC",
    description:
      "Notes on Refrigeration and AC for 1st or 2nd semester students",
    pdfLink: "machanical/me3.pdf",
  },
  {
    id: 21,
    subject: "Mechanical Engineering",
    year: "1st Year",
    title: "Fluid mechanics",
    description: "Notes on Fluid mechanics for 1st or 2nd semester students",
    pdfLink: "machanical/me4.pdf",
  },
  {
    id: 22,
    subject: "Mechanical Engineering",
    year: "1st Year",
    title: "Measurements",
    description: "Notes on Measurements for 1st or 2nd semester students",
    pdfLink: "machanical/me5.pdf",
  },
  {
    id: 23,
    subject: "Environment and ecology",
    year: "1st Year",
    title: "UNIT 1",
    description: "Notes for unit 1 1st or 2nd semester students",
    pdfLink: "Environment/evs1.pdf",
  },
  {
    id: 24,
    subject: "Environment and ecology",
    year: "1st Year",
    title: "UNIT 2",
    description: "Notes for unit 2 1st or 2nd semester students",
    pdfLink: "Environment/evs2.pdf",
  },
  {
    id: 25,
    subject: "Environment and ecology",
    year: "1st Year",
    title: "UNIT 3",
    description: "Notes for unit 3 1st or 2nd semester students",
    pdfLink: "Environment/evs3.pdf",
  },
  {
    id: 26,
    subject: "Environment and ecology",
    year: "1st Year",
    title: "UNIT 4",
    description: "Notes for unit 4 1st or 2nd semester students",
    pdfLink: "Environment/evs4.pdf",
  },
  {
    id: 27,
    subject: "Environment and ecology",
    year: "1st Year",
    title: "UNIT 5",
    description: "Notes for unit 5 1st or 2nd semester students",
    pdfLink: "Environment/evs5.pdf",
  },
  {
    id: 28,
    subject: "Electrical Engineering",
    year: "1st Year",
    title: "UNIT-2",
    description: "Notes on UNIT-2 for 1st or 2nd semester students",
    pdfLink: "BEE/ee2.pdf",
  },
  {
    id: 29,
    subject: "Electrical Engineering",
    year: "1st Year",
    title: "UNIT-3",
    description: "Notes on UNIT-3 for 1st or 2nd semester students",
    pdfLink: "BEE/ee3.pdf",
  },
  {
    id: 30,
    subject: "Electrical Engineering",
    year: "1st Year",
    title: "UNIT-4",
    description: "Notes on UNIT-4 for 1st or 2nd semester students",
    pdfLink: "BEE/ee4.pdf",
  },
  {
    id: 31,
    subject: "Electrical Engineering",
    year: "1st Year",
    title: "UNIT-5",
    description: "Notes on UNIT-5 for 1st or 2nd semester students",
    pdfLink: "BEE/ee5.pdf",
  },
  {
    id: 32,
    subject: "Programing for Problem Solving",
    year: "1st Year",
    title: "UNIT 2 Notes",
    description: "Notes on UNIT 2 for 1st or 2nd semester students",
    pdfLink: "pps/pps2.pdf",
  },
  {
    id: 33,
    subject: "Programing for Problem Solving",
    year: "1st Year",
    title: "UNIT 3 Notes",
    description: "Notes on UNIT 3 for 1st or 2nd semester students",
    pdfLink: "pps/pps3.pdf",
  },
  {
    id: 34,
    subject: "Programing for Problem Solving",
    year: "1st Year",
    title: "UNIT 4 Notes",
    description: "Notes on UNIT 4 for 1st or 2nd semester students",
    pdfLink: "pps/pps4.pdf",
  },
  {
    id: 35,
    subject: "Programing for Problem Solving",
    year: "1st Year",
    title: "UNIT 5 Notes",
    description: "Notes on UNIT 5 for 1st or 2nd semester students",
    pdfLink: "pps/pps5.pdf",
  },
  {
    id: 36,
    subject: "Electronic Engineering",
    year: "1st Year",
    title: "UNIT 1 Notes",
    description: "Notes on UNIT 5 for 1st or 2nd semester students",
    pdfLink: "fee/ec1.pdf",
  },
  {
    id: 37,
    subject: "Electronic Engineering",
    year: "1st Year",
    title: "UNIT 2 Notes",
    description: "Notes on UNIT 2 for 1st or 2nd semester students",
    pdfLink: "fee/ec2.pdf",
  },
  {
    id: 38,
    subject: "Electronic Engineering",
    year: "1st Year",
    title: "UNIT 3 Notes",
    description: "Notes on UNIT 3 for 1st or 2nd semester students",
    pdfLink: "fee/ec3.pdf",
  },
  {
    id: 39,
    subject: "Electronic Engineering",
    year: "1st Year",
    title: "UNIT 4 Notes",
    description: "Notes on UNIT 4 for 1st or 2nd semester students",
    pdfLink: "fee/ec4.pdf",
  },
  {
    id: 40,
    subject: "Electronic Engineering",
    year: "1st Year",
    title: "UNIT 5 Notes",
    description: "Notes on UNIT 5 for 1st or 2nd semester students",
    pdfLink: "fee/ec5.pdf",
  },
  {
    id: 41,
    subject: "soft skill",
    year: "1st Year",
    title: "UNIT 1 Notes",
    description: "Notes on UNIT 1 for 1st or 2nd semester students",
    pdfLink: "softkill/ss1.pdf",
  },
  {
    id: 42,
    subject: "soft skill",
    year: "1st Year",
    title: "UNIT 2 Notes",
    description: "Notes on UNIT 2 for 1st or 2nd semester students",
    pdfLink: "softkill/ss2.pdf",
  },
  {
    id: 43,
    subject: "soft skill",
    year: "1st Year",
    title: "UNIT 3 Notes",
    description: "Notes on UNIT 3 for 1st or 2nd semester students",
    pdfLink: "softkill/ss3.pdf",
  },
  {
    id: 44,
    subject: "soft skill",
    year: "1st Year",
    title: "UNIT 4 Notes",
    description: "Notes on UNIT 4 for 1st or 2nd semester students",
    pdfLink: "softkill/ss4.pdf",
  },
  {
    id: 45,
    subject: "soft skill",
    year: "1st Year",
    title: "UNIT 5 Notes",
    description: "Notes on UNIT 5 for 1st or 2nd semester students",
    pdfLink: "softkill/ss5.pdf",
  },
  // {
  //     id: 16,
  //     subject: "Mathematics",
  //     year: "2nd Year",
  //     title: "Calculus and Linear Algebra",
  //     description: "Notes on Calculus and Linear Algebra for 2nd semester students",
  //     pdfLink: "maths/maths2.pdf"
  // },
  // {
  //     id: 17,
  //     subject: "Programming",
  //     year: "2nd Year",
  //     title: "Introduction to Programming",
  //     description: "Notes on Introduction to Programming for 2nd semester students",
  //     pdfLink: "cs/intro_programming.pdf"
  // },
  // {
  //     id: 18,
  //     subject: "Electronics",
  //     year: "2nd Year",
  //     title: "Basic Electronics",
  //     description: "Notes on Basic Electronics for 2nd semester students",
  //     pdfLink: "electronics/basic_electronics.pdf"
  // },
  // {
  //     id: 19,
  //     subject: "Chemistry",
  //     year: "2nd Year",
  //     title: "Organic Chemistry",
  //     description: "Notes on Organic Chemistry for 2nd semester students",
  //     pdfLink: "chemistry/organic_chemistry.pdf"
  // },
  {
      id: 20,
      subject: "data structures",
      year: "2nd Year",
      title: "data structures",
      description: "Notes on data structures for all units",
      pdfLink: "dsa/Data-structure.pdf"
  },
  // {
  //     id: 21,
  //     subject: "Mathematics",
  //     year: "2nd Year",
  //     title: "Discrete Mathematics",
  //     description: "Notes on Discrete Mathematics for 3rd semester students",
  //     pdfLink: "maths/discrete_math.pdf"
  // },
  // {
  //     id: 22,
  //     subject: "Computer Science",
  //     year: "2nd Year",
  //     title: "Digital Logic Design",
  //     description: "Notes on Digital Logic Design for 3rd semester students",
  //     pdfLink: "cs/digital_logic.pdf"
  // },
  // {
  //     id: 23,
  //     subject: "Computer Science",
  //     year: "2nd Year",
  //     title: "Computer Organization",
  //     description: "Notes on Computer Organization for 3rd semester students",
  //     pdfLink: "cs/computer_org.pdf"
  // },
  // {
  //     id: 24,
  //     subject: "Computer Science",
  //     year: "2nd Year",
  //     title: "Design and Analysis of Algorithms",
  //     description: "Notes on Design and Analysis of Algorithms for 4th semester students",
  //     pdfLink: "cs/algorithms.pdf"
  // },
  // {
  //     id: 25,
  //     subject: "Computer Science",
  //     year: "2nd Year",
  //     title: "Operating Systems",
  //     description: "Notes on Operating Systems for 4th semester students",
  //     pdfLink: "cs/operating_systems.pdf"
  // },
  // {
  //     id: 26,
  //     subject: "Computer Science",
  //     year: "2nd Year",
  //     title: "Database Systems",
  //     description: "Notes on Database Systems for 4th semester students",
  //     pdfLink: "cs/database_systems.pdf"
  // },
  // {
  //     id: 27,
  //     subject: "Computer Science",
  //     year: "2nd Year",
  //     title: "Software Engineering",
  //     description: "Notes on Software Engineering for 4th semester students",
  //     pdfLink: "cs/software_engineering.pdf"
  // },
  // {
  //     id: 28,
  //     subject: "Computer Science",
  //     year: "3rd Year",
  //     title: "Computer Networks",
  //     description: "Notes on Computer Networks for 5th semester students",
  //     pdfLink: "cs/computer_networks.pdf"
  // },
  // {
  //     id: 29,
  //     subject: "Computer Science",
  //     year: "3rd Year",
  //     title: "Theory of Computation",
  //     description: "Notes on Theory of Computation for 5th semester students",
  //     pdfLink: "cs/theory_of_computation.pdf"
  // },
  // {
  //     id: 30,
  //     subject: "Computer Science",
  //     year: "3rd Year",
  //     title: "Microprocessors",
  //     description: "Notes on Microprocessors for 5th semester students",
  //     pdfLink: "cs/microprocessors.pdf"
  // },
  // {
  //     id: 31,
  //     subject: "Computer Science",
  //     year: "3rd Year",
  //     title: "Artificial Intelligence",
  //     description: "Notes on Artificial Intelligence for 5th semester students",
  //     pdfLink: "cs/artificial_intelligence.pdf"
  // },
  // {
  //     id: 32,
  //     subject: "Computer Science",
  //     year: "3rd Year",
  //     title: "Compiler Design",
  //     description: "Notes on Compiler Design for 6th semester students",
  //     pdfLink: "cs/compiler_design.pdf"
  // },
  // {
  //     id: 33,
  //     subject: "Computer Science",
  //     year: "3rd Year",
  //     title: "Web Technologies",
  //     description: "Notes on Web Technologies for 6th semester students",
  //     pdfLink: "cs/web_technologies.pdf"
  // },
  // {
  //     id: 34,
  //     subject: "Computer Science",
  //     year: "3rd Year",
  //     title: "Cryptography",
  //     description: "Notes on Cryptography for 6th semester students",
  //     pdfLink: "cs/cryptography.pdf"
  // },
  // {
  //     id: 35,
  //     subject: "Computer Science",
  //     year: "3rd Year",
  //     title: "Machine Learning",
  //     description: "Notes on Machine Learning for 6th semester students",
  //     pdfLink: "cs/machine_learning.pdf"
  // },
  // {
  //     id: 36,
  //     subject: "Computer Science",
  //     year: "4th Year",
  //     title: "Mobile Computing",
  //     description: "Notes on Mobile Computing for 7th semester students",
  //     pdfLink: "cs/mobile_computing.pdf"
  // },
  // {
  //     id: 37,
  //     subject: "Computer Science",
  //     year: "4th Year",
  //     title: "Cloud Computing",
  //     description: "Notes on Cloud Computing for 7th semester students",
  //     pdfLink: "cs/cloud_computing.pdf"
  // },
  // {
  //     id: 38,
  //     subject: "Computer Science",
  //     year: "4th Year",
  //     title: "Internet of Things",
  //     description: "Notes on Internet of Things for 7th semester students",
  //     pdfLink: "cs/iot.pdf"
  // },
  // {
  //     id: 39,
  //     subject: "Computer Science",
  //     year: "4th Year",
  //     title: "Cyber Security",
  //     description: "Notes on Cyber Security for 7th semester students",
  //     pdfLink: "cs/cyber_security.pdf"
  // },
  // {
  //     id: 40,
  //     subject: "Computer Science",
  //     year: "4th Year",
  //     title: "Big Data Analytics",
  //     description: "Notes on Big Data Analytics for 8th semester students",
  //     pdfLink: "cs/big_data.pdf"
  // },
  // {
  //     id: 41,
  //     subject: "Computer Science",
  //     year: "4th Year",
  //     title: "Blockchain Technology",
  //     description: "Notes on Blockchain Technology for 8th semester students",
  //     pdfLink: "cs/blockchain.pdf"
  // },
  // {
  //     id: 42,
  //     subject: "Computer Science",
  //     year: "4th Year",
  //     title: "Quantum Computing",
  //     description: "Notes on Quantum Computing for 8th semester students",
  //     pdfLink: "cs/quantum_computing.pdf"
  // },
  // {
  //     id: 43,
  //     subject: "Computer Science",
  //     year: "4th Year",
  //     title: "Advanced Algorithms",
  //     description: "Notes on Advanced Algorithms for 8th semester students",
  //     pdfLink: "cs/advanced_algorithms.pdf"
  // }
];

// Function to generate the list of notes
function generateNoteList(filteredNotes) {
  const noteList = document.getElementById("note-list");
  noteList.innerHTML = "";
  filteredNotes.forEach((note) => {
    const listItem = document.createElement("li");
    listItem.innerHTML = `
            <h3>${note.title}</h3>
            <p><strong>Subject:</strong> ${note.subject}</p>
            <p><strong>year:</strong> ${note.year}</p>
            <p>${note.description}</p>
            <button>
               <span> <a href="${note.pdfLink}" download>downlode</a></span>
               <svg width="34" height="34" viewBox="0 0 74 74" fill="none" xmlns="http://www.w3.org/2000/svg">
                   <circle cx="37" cy="37" r="35.5" stroke="black" stroke-width="3"></circle>
                   <path d="M25 35.5C24.1716 35.5 23.5 36.1716 23.5 37C23.5 37.8284 24.1716 38.5 25 38.5V35.5ZM49.0607 38.0607C49.6464 37.4749 49.6464 36.5251 49.0607 35.9393L39.5147 26.3934C38.9289 25.8076 37.9792 25.8076 37.3934 26.3934C36.8076 26.9792 36.8076 27.9289 37.3934 28.5147L45.8787 37L37.3934 45.4853C36.8076 46.0711 36.8076 47.0208 37.3934 47.6066C37.9792 48.1924 38.9289 48.1924 39.5147 47.6066L49.0607 38.0607ZM25 38.5L48 38.5V35.5L25 35.5V38.5Z" fill="black"></path>
               </svg>
           </button>
           
            
        `;
    noteList.appendChild(listItem);
  });
}

// Event listener for the filter button
document.getElementById("apply-filter").addEventListener("click", () => {
  const subject = document.getElementById("subject-filter").value;
  const year = document.getElementById("year-filter").value;
  const filteredNotes = notes.filter((note) => {
    return (
      (subject === "" || note.subject === subject) &&
      notes.filter((note) => note.year === year)
    );
  });
  generateNoteList(filteredNotes);
});

// Initial load with all notes
generateNoteList(notes);

// async function fetchNotes(subject, year) {
//     const response = await fetch(`https://api.openstax.org/v1/content?subject=${subject}&year${year}`);
//     const data = await response.json();
//     const notes = data.hits.hits.map(record => ({
//         title: record.metadata.title,
//         subject: subject,
//         year: year,
//         description: record.metadata.description,
//         pdfLink : record.files[0].links.download
//     }));
//     return notes;
// }

// Initial load with all notes
generateNoteList(filteredNotes);
