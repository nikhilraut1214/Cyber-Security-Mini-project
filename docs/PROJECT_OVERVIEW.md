# Project Overview: Mobile Data Leakage Prevention Console

**Repository:** https://github.com/nikhilraut1214/Cyber-Security-Mini-project  
**Document:** Project Overview & Scope Specification  
**Version:** 1.1.0  
**Last Updated:** 2026-10-23  

---

## 1. Executive Summary

The **Mobile Data Leakage Prevention (DLP) Console** is an educational, explainable software simulation engineered for computer science cybersecurity coursework. It demonstrates how modern organizations employ Mobile Device Management (MDM) policies and endpoint Data Loss Prevention (DLP) mechanisms to prevent unauthorized exfiltration of sensitive information from mobile devices.

The application joins two complementary security controls under a centralized operational dashboard:
1. **Pre-Installation Permission Risk Analysis:** Inspects requested application permissions against least-privilege category baselines to identify over-privileged applications before installation.
2. **Outbound Data Leakage Prevention:** Inspects egress text payloads for sensitive patterns (payment cards, government identification numbers, phone numbers, and email addresses) to enforce masking or blocking policies.

---

## 2. Problem Statement & Real-World Context

### The Challenge of Over-Privileged Mobile Apps
Mobile operating systems utilize permission systems to restrict access to sensitive device APIs (camera, microphone, geolocation, contacts, SMS). However, end-users routinely grant broad permissions to applications without understanding their privacy implications. Unscrupulous application developers frequently request permissions far beyond the functional requirements of their software to harvest user data for monetization.

### The Anchor Case Study: FTC vs. Brightest Flashlight Free (2013–2014)
A foundational case study inspiring this project is the United States Federal Trade Commission (FTC) enforcement action against GoldenShores Technologies, LLC, the creators of the popular "Brightest Flashlight Free" Android application:
- **The Deception:** The application's privacy policy stated that personal information was used exclusively for internal product operations. In reality, the app secretly transmitted the device's precise GPS coordinates and persistent device identifiers (IMEI) to third-party advertising networks the moment the application was launched.
- **The Security Lesson:** A flashlight application requires only camera hardware access to activate the LED flash. Access to fine geolocation, telephony identifiers, and contact data constitutes an overt least-privilege violation that enterprise MDM software should flag and intercept.

---

## 3. Project Objectives

1. **Demonstrate Explainable Least-Privilege Heuristics:** Implement transparent, weighted scoring rules that evaluate Android application permissions against category baselines and categorize risk as Low (`Allow`), Medium (`Review`), or High (`Block`).
2. **Demonstrate Pattern-Based Egress Filtering:** Implement regular-expression pattern detection combined with mathematical validation (Luhn checksum) to intercept sensitive outbound text without persisting sensitive content.
3. **Simulate Enterprise MDM Lifecycle Controls:** Model core administrative controls including policy enforcement, an administrative approval queue for borderline applications, remote device wiping, and re-enrolment.
4. **Maintain Privacy in Audit Telemetry:** Enforce a strict privacy model in audit logging by recording only decision types, timestamps, and finding counts, ensuring raw payload values are never stored.
5. **Academic & Demonstration Readiness:** Provide an offline, self-contained application runnable with a single command, accompanied by a 5-minute repeatable demonstration script.

---

## 4. Target Audience

- **Course Evaluators & Instructors:** Reviewing the technical implementation, architectural cleanliness, heuristic design, and automated test coverage.
- **Demonstration Audiences:** Following the logical progression from over-privileged flashlight installation to outbound data interception.
- **Student Maintainers & Recruiters:** Inspecting code quality, architectural decoupling, test suite completeness, and technical documentation.

---

## 5. Scope & Explicit Non-Goals

| In Scope (Simulated Heuristics) | Out of Scope (Non-Goals) |
| :--- | :--- |
| In-memory simulation of Android package permissions | Managing physical Android devices or installing real `.apk` files |
| Static heuristic rules evaluating least-privilege violations | Dynamic runtime analysis, sandbox execution, or taint tracking |
| Regular expression and Luhn checksum pattern detection | Deep packet inspection, TLS interception, or network firewalls |
| Simulated device remote wipe and re-enrolment | Real hardware MDM enrollment profiles (e.g., Android Enterprise API) |
| Non-retention audit logging and CSV export | Persistent external relational databases or cloud telemetry backends |
| Synthetic, non-personal test data only | Processing real personal data, actual credit cards, or production secrets |

> **Critical Notice:** This project is strictly an educational software simulation. It does not control physical mobile devices, make network API calls, or replace commercial MDM or DLP solutions.
