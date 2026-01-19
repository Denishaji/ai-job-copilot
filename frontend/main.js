// frontend/main.js

const BACKEND_BASE_URL = "http://localhost:8001";

const resumeFileInput = document.getElementById("resume-file");
const uploadResumeBtn = document.getElementById("upload-resume-btn");
const clearResumeBtn = document.getElementById("clear-resume-btn");
const resumeTextArea = document.getElementById("resume-text");

const jdTextArea = document.getElementById("jd-text");
const analyzeBtn = document.getElementById("analyze-btn");
const statusSpan = document.getElementById("status");

const resultEmpty = document.getElementById("result-empty");
const resultContent = document.getElementById("result-content");
const matchScoreSpan = document.getElementById("match-score");
const matchLevelSpan = document.getElementById("match-level");
const atsScoreSpan = document.getElementById("ats-score");
const analysisTextP = document.getElementById("analysis-text");
const matchedSkillsDiv = document.getElementById("matched-skills");
const missingSkillsDiv = document.getElementById("missing-skills");
const resumeSuggestionsUl = document.getElementById("resume-suggestions");
const extraKeywordsDiv = document.getElementById("extra-keywords");

function setStatus(message) {
  statusSpan.textContent = message || "";
}

function clearResult() {
  resultEmpty.style.display = "block";
  resultContent.style.display = "none";
  matchScoreSpan.textContent = "";
  matchLevelSpan.textContent = "";
  atsScoreSpan.textContent = "";
  analysisTextP.textContent = "";
  matchedSkillsDiv.innerHTML = "";
  missingSkillsDiv.innerHTML = "";
  resumeSuggestionsUl.innerHTML = "";
  extraKeywordsDiv.innerHTML = "";
}

clearResult();

uploadResumeBtn.addEventListener("click", async () => {
  setStatus("");
  clearResult();

  const file = resumeFileInput.files[0];
  if (!file) {
    setStatus("Please choose a PDF resume first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    setStatus("Uploading and extracting resume text...");
    const response = await fetch(`${BACKEND_BASE_URL}/profile/upload_resume`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      setStatus(errorData.detail || "Failed to upload or parse resume.");
      return;
    }

    const data = await response.json();
    resumeTextArea.value = data.resume_text || "";
    setStatus("Resume text extracted. You can edit it if needed.");
  } catch (err) {
    console.error(err);
    setStatus("Error connecting to backend. Is it running on 127.0.0.1:8001?");
  }
});

clearResumeBtn.addEventListener("click", () => {
  resumeTextArea.value = "";
  setStatus("");
  clearResult();
});

analyzeBtn.addEventListener("click", async () => {
  setStatus("");
  clearResult();

  const jobDescription = jdTextArea.value.trim();
  const candidateProfile = resumeTextArea.value.trim();

  if (!jobDescription) {
    setStatus("Please paste a job description.");
    return;
  }
  if (!candidateProfile) {
    setStatus("Please upload your resume and/or paste resume text.");
    return;
  }

  try {
    setStatus("Analyzing job and resume...");
    const response = await fetch(`${BACKEND_BASE_URL}/jobs/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        job_description: jobDescription,
        candidate_profile: candidateProfile,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      setStatus(errorData.detail || "Job analysis failed.");
      return;
    }

    const data = await response.json();
    renderResult(data.parsed_job, data.analysis);
    setStatus("Analysis complete.");
  } catch (err) {
    console.error(err);
    setStatus("Error connecting to backend. Is it running on 127.0.0.1:8001?");
  }
});

function renderResult(parsedJob, analysisText) {
  if (!parsedJob) {
    setStatus("No parsed job data returned.");
    return;
  }

  resultEmpty.style.display = "none";
  resultContent.style.display = "block";

  matchScoreSpan.textContent =
    typeof parsedJob.match_score === "number" ? parsedJob.match_score : "-";
  matchLevelSpan.textContent = parsedJob.match_level || "-";
  atsScoreSpan.textContent =
    typeof parsedJob.ats_score === "number" ? parsedJob.ats_score : "-";

  analysisTextP.textContent = analysisText || parsedJob.analysis || "";

  matchedSkillsDiv.innerHTML = "";
  (parsedJob.matched_skills || []).forEach((skill) => {
    const span = document.createElement("span");
    span.className = "tag";
    span.textContent = skill;
    matchedSkillsDiv.appendChild(span);
  });

  missingSkillsDiv.innerHTML = "";
  (parsedJob.missing_skills || []).forEach((skill) => {
    const span = document.createElement("span");
    span.className = "tag";
    span.textContent = skill;
    missingSkillsDiv.appendChild(span);
  });

  resumeSuggestionsUl.innerHTML = "";
  (parsedJob.resume_suggestions || []).forEach((s) => {
    const li = document.createElement("li");
    li.textContent = s;
    resumeSuggestionsUl.appendChild(li);
  });

  extraKeywordsDiv.innerHTML = "";
  (parsedJob.extra_resume_keywords || []).forEach((kw) => {
    const span = document.createElement("span");
    span.className = "tag";
    span.textContent = kw;
    extraKeywordsDiv.appendChild(span);
  });
}
