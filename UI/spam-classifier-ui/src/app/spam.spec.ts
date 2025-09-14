import { TestBed } from '@angular/core/testing';

import { Spam } from './spam';

describe('Spam', () => {
  let service: Spam;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Spam);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
