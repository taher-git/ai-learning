import { TestBed } from '@angular/core/testing';

import { DocAssistantService } from './doc-assistant-service';

describe('DocAssistantService', () => {
  let service: DocAssistantService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DocAssistantService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
