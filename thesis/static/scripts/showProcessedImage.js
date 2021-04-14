window.onload = init;

			function init() {
				
				// Get div that stores image, and the image itself
				var classImageBox = document.getElementById("classimageframe");
				var neurImageBox = document.getElementById("neurimageframe");
				var classSourceImage = document.getElementById("classsourceimage");
				var neurSourceImage = document.getElementById("neursourceimage");
 							
				// If the user has the cookie given by this site
				if (document.cookie.indexOf("IID") >= 0) {

					// Show div containing image, change image to processed image submitted
					// by user
					classImageBox.style.display = "block";
					neurImageBox.style.display = "block";
					classSourceImage.src = "static/faces/processed_images/classifier_images/".concat(getCookie("IID"))
					neurSourceImage.src = "static/faces/processed_images/classifier_images/".concat(getCookie("IID"))
					}
					else {
					
					// Keep image div hidden
					classImageBox.style.display = "none";
					neurImageBox.style.display = "none";
				
				}

			
			}

			// v----------v CODE ADAPTED FROM W3SCHOOLS.COM v----------v
			function getCookie(c_name) {
				
				if (document.cookie.length > 0) {
					
					c_start = document.cookie.indexOf(c_name + "=");
					
					if (c_start != -1) {
						
						c_start = c_start + c_name.length + 1;
						c_end = document.cookie.indexOf(";", c_start);
						
						if (c_end == -1) {
							
							c_end = document.cookie.length;
						
						}
						
						return unescape(document.cookie.substring(c_start, c_end));
					
					}
				
				}
	
				return "";

			}
			// ^----------^ CODE ADAPTED FROM W3SCHOOLS.COM ^----------^