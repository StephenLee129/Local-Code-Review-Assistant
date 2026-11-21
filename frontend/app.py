
import streamlit as st
import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Local Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)

def submit_code_for_review(code: str) -> dict:
    """Submit source code to the backend and return the review."""

    response = requests.post(
        f"{API_BASE_URL}/review",
        json={"code": code},
        timeout=120
    )

    response.raise_for_status()

    return response.json()


def main():
    st.title("Local Code Review Assistant")
    st.write(
        "Analyze your source code using a locally hosted AI model."
    )

    st.subheader("Source Code")

    code = st.text_area(
        "Paste your code below:",
        height=400,
        placeholder="Enter your source code here..."
    )

    if st.button("Review Code", type="primary"):
        if not code.strip():
            st.warning("Please enter some source code first.")
        else:
            try:
                with st.spinner("Analyzing your code..."):
                    review = submit_code_for_review(code)

                st.success("Code review completed!")

                st.subheader("Summary")
                st.write(review["summary"])

                st.subheader("Issues")

                if not review["issues"]:
                    st.success("No issues found!")
                else:
                    for issue in review["issues"]:
                        st.markdown(f"**{issue['title']}**")

                        st.caption(
                            f"Severity: {issue['severity'].upper()}"
                        )

                        st.write(issue["description"])

                        st.markdown(
                            f"**Suggestion:** {issue['suggestion']}"
                        )

                        if issue["line_number"] is not None:
                            st.caption(
                                f"Approximate line: {issue['line_number']}"
                            )

                        st.divider()

            except requests.exceptions.Timeout:
                st.error("The code review timed out. Please try again.")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the backend. "
                    "Make sure the FastAPI server is running."
                )

            except requests.exceptions.HTTPError as error:
                st.error(f"The backend returned an error: {error}")

            except (KeyError, ValueError):
                st.error("The backend returned an unexpected response.")


if __name__ == "__main__":
    main()
