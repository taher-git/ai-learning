import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReviewHistory } from './review-history';

describe('ReviewHistory', () => {
  let component: ReviewHistory;
  let fixture: ComponentFixture<ReviewHistory>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReviewHistory]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReviewHistory);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
