"""
Accessibility Testing Utility
WCAG 2.1 compliance checking and accessibility testing
"""
from playwright.sync_api import Page
from typing import Dict, List
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class AccessibilityChecker:
    """Check web pages for accessibility compliance."""
    
    def __init__(self, page: Page):
        """
        Initialize accessibility checker.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        
    def check_page_accessibility(self) -> Dict:
        """
        Run accessibility checks on current page.
        
        Returns:
            Dictionary containing accessibility violations
        """
        logger.info("Running accessibility checks")
        
        violations = {
            'missing_alt_text': self._check_missing_alt_text(),
            'missing_labels': self._check_missing_form_labels(),
            'low_contrast': self._check_color_contrast(),
            'missing_headings': self._check_heading_structure(),
            'missing_landmarks': self._check_landmarks(),
            'keyboard_accessibility': self._check_keyboard_navigation()
        }
        
        total_violations = sum(len(v) for v in violations.values() if isinstance(v, list))
        logger.info(f"Accessibility check complete. Total violations: {total_violations}")
        
        return violations
        
    def _check_missing_alt_text(self) -> List[str]:
        """Check for images without alt text."""
        images_without_alt = self.page.locator('img:not([alt])').all()
        violations = []
        
        for img in images_without_alt:
            src = img.get_attribute('src') or 'unknown'
            violations.append(f"Image missing alt text: {src}")
            
        if violations:
            logger.warning(f"Found {len(violations)} images without alt text")
            
        return violations
        
    def _check_missing_form_labels(self) -> List[str]:
        """Check for form inputs without labels."""
        inputs = self.page.locator('input:not([type="hidden"]):not([aria-label]):not([aria-labelledby])').all()
        violations = []
        
        for inp in inputs:
            input_id = inp.get_attribute('id') or inp.get_attribute('name') or 'unknown'
            # Check if input has associated label
            if input_id != 'unknown':
                label = self.page.locator(f'label[for="{input_id}"]').count()
                if label == 0:
                    violations.append(f"Input without label: {input_id}")
            else:
                violations.append("Input without id/name and no label")
                
        if violations:
            logger.warning(f"Found {len(violations)} inputs without labels")
            
        return violations
        
    def _check_color_contrast(self) -> List[str]:
        """Check for potential color contrast issues."""
        # This is a simplified check - in production, use axe-core or similar
        violations = []
        
        # Check for common low-contrast patterns
        low_contrast_selectors = [
            '.text-muted',
            '.text-secondary',
            '[style*="color: #999"]',
            '[style*="color: #ccc"]'
        ]
        
        for selector in low_contrast_selectors:
            elements = self.page.locator(selector).count()
            if elements > 0:
                violations.append(f"Potential low contrast: {selector} ({elements} elements)")
                
        return violations
        
    def _check_heading_structure(self) -> List[str]:
        """Check for proper heading hierarchy."""
        violations = []
        
        # Check if page has h1
        h1_count = self.page.locator('h1').count()
        if h1_count == 0:
            violations.append("Page missing h1 heading")
        elif h1_count > 1:
            violations.append(f"Page has multiple h1 headings ({h1_count})")
            
        # Check heading order
        headings = self.page.locator('h1, h2, h3, h4, h5, h6').all()
        prev_level = 0
        
        for heading in headings:
            tag = heading.evaluate('el => el.tagName.toLowerCase()')
            level = int(tag[1])
            
            if prev_level > 0 and level > prev_level + 1:
                violations.append(f"Heading hierarchy skip: {tag} after h{prev_level}")
                
            prev_level = level
            
        return violations
        
    def _check_landmarks(self) -> List[str]:
        """Check for ARIA landmarks."""
        violations = []
        
        # Check for main landmark
        if self.page.locator('main, [role="main"]').count() == 0:
            violations.append("Page missing main landmark")
            
        # Check for navigation landmark
        if self.page.locator('nav, [role="navigation"]').count() == 0:
            violations.append("Page missing navigation landmark")
            
        return violations
        
    def _check_keyboard_navigation(self) -> List[str]:
        """Check for keyboard accessibility issues."""
        violations = []
        
        # Check for interactive elements without keyboard support
        clickable_divs = self.page.locator('div[onclick]:not([tabindex]):not([role="button"])').count()
        if clickable_divs > 0:
            violations.append(f"Found {clickable_divs} clickable divs without keyboard support")
            
        # Check for links without href
        empty_links = self.page.locator('a:not([href])').count()
        if empty_links > 0:
            violations.append(f"Found {empty_links} links without href")
            
        return violations
        
    def generate_accessibility_report(self) -> str:
        """
        Generate accessibility report.
        
        Returns:
            Formatted accessibility report
        """
        violations = self.check_page_accessibility()
        
        report = ["=" * 50]
        report.append("ACCESSIBILITY REPORT")
        report.append("=" * 50)
        report.append(f"Page: {self.page.url}")
        report.append("")
        
        total_violations = 0
        for category, issues in violations.items():
            if issues:
                report.append(f"\n{category.replace('_', ' ').title()}:")
                report.append("-" * 40)
                for issue in issues:
                    report.append(f"  • {issue}")
                    total_violations += 1
                    
        report.append("")
        report.append("=" * 50)
        report.append(f"Total Violations: {total_violations}")
        report.append("=" * 50)
        
        report_text = "\n".join(report)
        logger.info(f"Accessibility report generated with {total_violations} violations")
        
        return report_text
