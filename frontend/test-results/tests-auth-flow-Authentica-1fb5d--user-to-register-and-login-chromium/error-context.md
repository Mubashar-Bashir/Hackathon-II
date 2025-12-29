# Page snapshot

```yaml
- generic [ref=e1]:
  - generic [ref=e3]:
    - generic [ref=e4]:
      - generic [ref=e7]: T
      - heading "Create Account" [level=1] [ref=e8]
      - paragraph [ref=e9]: Join us to manage your tasks
    - generic [ref=e10]:
      - generic [ref=e11]:
        - generic [ref=e12]:
          - generic [ref=e13]: Name
          - textbox "Your name" [ref=e14]
        - generic [ref=e15]:
          - generic [ref=e16]: Email
          - textbox "your@email.com" [active] [ref=e17]
        - generic [ref=e18]:
          - generic [ref=e19]: Password
          - textbox "••••••••" [ref=e20]: SecurePassword123!
        - generic [ref=e21]:
          - generic [ref=e22]: Confirm Password
          - textbox "••••••••" [ref=e23]: SecurePassword123!
      - button "Sign Up" [ref=e24]
    - generic [ref=e25]:
      - text: Already have an account?
      - link "Sign in" [ref=e26] [cursor=pointer]:
        - /url: /login
  - button "Open Next.js Dev Tools" [ref=e32] [cursor=pointer]:
    - img [ref=e33]
  - alert [ref=e36]
```