import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Summarizer } from './summarizer';

describe('Summarizer', () => {
  let component: Summarizer;
  let fixture: ComponentFixture<Summarizer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Summarizer]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Summarizer);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
