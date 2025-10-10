import { TestBed } from '@angular/core/testing';

import { CodeReviewerService } from './code-reviewer-service';

describe('CodeReviewerService', () => {
  let service: CodeReviewerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CodeReviewerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
