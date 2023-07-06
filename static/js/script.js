function handleUserSelection() {
    const dropdown = document.getElementById("user-dropdown");
    const selectedOption = dropdown.value;
  
    if (selectedOption === "add-user") {
      window.location.href = "/add-user";
    } else if (selectedOption === "manage-users") {
      window.location.href = "/manage-users";
    }
  }
  