// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
//
// It adds an "Urgency" cell and a "Result" cell right after the deadline cell.
// The labels only depend on days_left (team rule), not on the status.
function showDeadline(row, cell, opportunity) {
  const urgencyCell = document.createElement("td");
  const resultCell = document.createElement("td");
  cell.after(urgencyCell, resultCell);

  const daysLeft = opportunity.days_left;
  showResult(resultCell, daysLeft);
  let text = "";
  let colour = "";

  if (daysLeft < 0) {
    text = "Overdue";
    colour = "overdue";
  } else if (daysLeft === 0) {
    text = "Due today";
    colour = "today";
  } else if (daysLeft <= 7) {
    text = daysLeft === 1 ? "Due in 1 day" : "Due in " + daysLeft + " days";
    colour = "soon";
  }

  // Deadlines more than 7 days away get no label.
  if (text === "") {
    return;
  }

  const label = document.createElement("span");
  label.className = "deadline-label deadline-" + colour;
  label.textContent = text;
  urgencyCell.appendChild(label);
}

// Fills the Result cell: "Fail" if the deadline has passed, "Pass" if not.
function showResult(resultCell, daysLeft) {
  const label = document.createElement("span");
  if (daysLeft < 0) {
    label.className = "deadline-label result-fail";
    label.textContent = "Fail";
  } else {
    label.className = "deadline-label result-pass";
    label.textContent = "Pass";
  }
  resultCell.appendChild(label);
}

// Adds the "Urgency" and "Result" column headings after the "Deadline" heading.
function addHeadings() {
  const headings = document.querySelectorAll("thead th");
  for (const heading of headings) {
    if (heading.textContent === "Deadline") {
      const urgencyHeading = document.createElement("th");
      urgencyHeading.textContent = "Urgency";
      const resultHeading = document.createElement("th");
      resultHeading.textContent = "Result";
      heading.after(urgencyHeading, resultHeading);
    }
  }
}

addHeadings();
